instruction="###Instruction###\n\
Please act as an impartial and helpful evaluator for natural language generation (NLG), and the audience is an expert in the field.\n\
Your task is to evaluate the quality of {task} strictly based on the given evaluation criterion.\n\
Begin the evaluation by providing your analysis concisely and accurately, and then on the next line, start with \"Rating:\" followed by your rating on a Likert scale from 1 to 5 (higher means better).\n\
You MUST keep to the strict boundaries of the evaluation criterion and focus solely on the issues and errors involved; otherwise, you will be penalized.\n\
Make sure you read and understand these instructions, as well as the following evaluation criterion and example content, carefully.\n\
\n\
###Evaluation Criterion###\n\
{aspect}\n\
\n\
###Example###\n\
{source_des}:\n\
{source}\n\
\n\
{target_des}:\n\
{target}\n\
\n\
###Your Evaluation###\n"


import json
from vllm import LLM, SamplingParams  


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
            "sub_obj": sub_obj_key,  
            "scores": scores,
            "text": text
        })
        

        instruction_ = instruction.format(task="Story Generation", aspect="Anything", source_des="Story Prompt", source=origin_prompt, target_des="Generated Story", target=text)
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
        model="../Themis", 
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

with open("../Themis_OPENMEVA.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")