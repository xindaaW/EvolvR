instruction="""
You are evaluating Story Evaluation task. 
The input of model is "{src}". The model generated output is "{out}\n".
Please identify all errors within each model output, up to a maximum of five. 
For each error, please give me the corresponding error dimension, error type, major/minor label, error location of the model generated output and explanation for the error. 
Major errors can confuse or mislead the reader due to significant change in meaning, while minor errors don't lead to loss of meaning but will be noticed."""


from vllm import LLM, SamplingParams
import json 

pe = []
file_path = "../HANNA_test.json"  
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
        # score = sample["score"]
        # prompt = "Please write a story."
        prompt = sample["prompt"]
        prompts_fewshot_ = instruction.format(src=prompt, out=context)
        pe.append(prompts_fewshot_)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../TIGERScore-13B", tensor_parallel_size=4)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    instruction_ = instruction.format(src=prompt, out=context)
    output_text = f"## Output\n {generated_text}\n  <TRUE_ANSWER>{item['score']}</TRUE_ANSWER>"

    result_item = {
        "instruction": instruction_,
        "input": "",
        "output": output_text
    }
    result.append(result_item)
    
with open("../Tiger13B_HANNA.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")



