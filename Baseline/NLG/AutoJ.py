instruction= """Write critiques for a submitted response on a given user's query, and grade the response:
  
[BEGIN DATA]
***
[Query]: {prompt}
***
[Response]: {response}
***
[END DATA]

Write critiques for this response. After that, you should give a final rating for the response on a scale of 1 to 10 by strictly following this format: "[[rating]]", for example: "Rating: [[5]]"."""


from vllm import LLM, SamplingParams
import json 

pe = []
file_path = "../StoryER_test.json"  


with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    if not data or not isinstance(data[0], dict):
        print("Data format does not meet expectations, please check JSON file structure")
        exit(1)
        
    total_samples = len(data)
    print(f"Loaded {total_samples} samples")
    
    for sample in data:
        context = sample["context"]
        aspect = sample["aspect"]
        score = sample["score"]
        # prompt = sample["prompt"]
        prompt = "write a story."
        # instruction_ = instruction.format(context=context, aspect=aspect, prompt=prompt)
        instruction_ = instruction.format(response=context, prompt=prompt)
        pe.append(instruction_)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../autoj-13b", tensor_parallel_size=4, gpu_memory_utilization=0.8)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    # instruction_ = instruction.format(context=item['context'], aspect=item['aspect'], prompt=item['prompt'])
    instruction_ = instruction.format(response=context, prompt=prompt)

    result_item = {
        "instruction": instruction_,
        "output": generated_text,
        "final score": item['score']
    }
    result.append(result_item)
    
with open("../autoj_13B_Point_StoryER.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")