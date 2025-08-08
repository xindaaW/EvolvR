pe = """
# Goals
You are an expert in story evaluation questions. Currently, there is a story content and story evaluation content. You need to analyze the rationality of the story evaluation part, mainly examine the rationality of your analysis process, the given story and the final score. The final score is unquestionable. If there is a problem, you need to modify the analysis process.
# Input
## Story Evaluation Requirements
{instruction}
## Story Analysis Process
{output}
# OutputFormat
[Problem Discovery]

[Revised Result]

# Workflow
1、Output [Problem Discovery]: Carefully review your output process to check for problems in the process. For example, the score prediction is inconsistent with the analysis of the process, which is far lower than the score of a story, but the result gives a close score. Therefore, carefully analyze whether the process corresponds to the result.
2、Output [Revised Result]: Refer to the previous output format and the results of [Problem Discovery], revise and unpdate the story analysis process but do not change the score. It is required that the final score remains unchanged. 
** Note that the final score is absolutely correct. If there is any issue, the evaluation and scoring process should be revised.
"""
import json
import os
import re
import vllm
from tqdm import tqdm

from vllm import LLM, SamplingParams
import json 

def extract_string(text):
    start_tag = "[Revised Result]"
    end_tag = "</Score2_TRUE_ANSWER>"

    start_index = text.find(start_tag)

    if start_index == -1:
        print(f"Error: Start tag '{start_tag}' not found")
        return None

    content_start = start_index + len(start_tag)

    end_index = text.find(end_tag, content_start)

    if end_index == -1:
        print(f"Error: End tag '{end_tag}' not found")
        return None

    extracted_string = text[content_start : end_index + len(end_tag)]

    return extracted_string

def extract_score(text):
    start_pos = text.find('<Score1_TRUE_ANSWER>')
    tail_part = ""
    if start_pos != -1:
        tail_part = text[start_pos:]
    return tail_part

peList = []
file_path = "../AfterRuleCheck.json"  

data = []
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
except json.JSONDecodeError:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:  
                data.append(json.loads(line))
    print(f"Detected JSON Lines format, loaded {len(data)} samples")
except Exception as e:
    print(f"File loading failed: {str(e)}")
    exit(1)

total_samples = len(data)
print(f"Loaded {total_samples} samples")
    
for item in data:
    instruction = item['instruction']
    output = item['output']
    prompt = pe.format(instruction=instruction, output=output)
    peList.append(prompt)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=3000, repetition_penalty=1)
llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4, gpu_memory_utilization=0.55)
outputs = llm.generate(peList, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    res = extract_string(generated_text)
    score = extract_score(item['output'])
    result_item = {
        "instruction": item['instruction'],
        "input": "",
        "output": res,
        "score": score
    }
    result.append(result_item)

with open("../AfterSelfCheck.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")
