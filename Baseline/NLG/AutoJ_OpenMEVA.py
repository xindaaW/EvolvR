instruction= """Write critiques for a submitted response on a given user's query, and grade the response:
  
[BEGIN DATA]
***
[Query]: {prompt}
***
[Response]: {response}
***
[END DATA]

Write critiques for this response. After that, you should give a final rating for the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]"."""

import json
from vllm import LLM, SamplingParams  # 或其他LLM库


file_path = "../mans_wp.json"
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

pe = []                
score_records = []     
sample_id = 0          

for top_key, top_value in data.items():

    if "gen" not in top_value:
        continue
    gen_obj = top_value["gen"]
    origin_prompt = top_value["prompt"]

    for sub_obj_key, sub_obj_value in gen_obj.items():
        text = sub_obj_value.get("text", "")
        scores = sub_obj_value.get("score", [])
        
        if not text or not scores:  
            continue
        
        score_records.append({
            "top_key": top_key,
            "sub_obj": sub_obj_key,  # e.g. "gpt", "plan_write"
            "scores": scores,
            "text": text
        })
        
        instruction_ = instruction.format(response=text, prompt=origin_prompt)
        pe.append(instruction_)

print(f"Valid samples: {len(pe)}")
print(f"First prompt: {pe[0] if pe else 'None'}")

if not pe:
    print("No valid samples, skip inference")
else:
    sampling_params = SamplingParams(
        temperature=1, 
        top_p=0.95, 
        max_tokens=1000, 
        repetition_penalty=1
    )
    llm = LLM(
        model="../autoj-13b", 
        tensor_parallel_size=4, 
        gpu_memory_utilization=0.8
    )
    outputs = llm.generate(pe, sampling_params)

    result = []
    for i, output in enumerate(outputs):
        generated_text = output.outputs[0].text
        record = score_records[i]  
        
        avg_score = sum(record["scores"]) / len(record["scores"])
        
        result_item = {
            "instruction": pe[i],          
            "output": generated_text,      
            "top_key": record["top_key"],  
            "sub_obj": record["sub_obj"],  
            "original_text": record["text"],  
            "scores": record["scores"],    
            "avg_score": avg_score         
        }
        result.append(result_item)
        
with open("../autoj_13B_Point_OpenMEVA.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")