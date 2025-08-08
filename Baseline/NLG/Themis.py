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
        # score = sample["score"]
        prompt = "Please write a story."
        prompts_fewshot_ = instruction.format(task="Story Generation", aspect=aspect, source_des="Story Prompt", source=prompt, target_des="Generated Story", target=context)
        pe.append(prompts_fewshot_)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../Themis", tensor_parallel_size=4)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    instruction_ = instruction.format(task="Story Generation", aspect=aspect, source_des="Story Prompt", source=prompt, target_des="Generated Story", target=context)
    output_text = f"## Output\n {generated_text}\n  <TRUE_ANSWER>{item['score']}</TRUE_ANSWER>"

    result_item = {
        "instruction": instruction_,
        "input": "",
        "output": output_text
    }
    result.append(result_item)
    
with open("../Themis_StoryER.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")