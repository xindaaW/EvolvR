import json
import os
import re
import vllm
from tqdm import tqdm

from vllm import LLM, SamplingParams

def remap_scores_to_1_and_5(output_str):


    match1 = re.search(r"(<Score1_TRUE_ANSWER>\s*)(\d+)(\s*</Score1_TRUE_ANSWER>)", output_str)
    match2 = re.search(r"(<Score2_TRUE_ANSWER>\s*)(\d+)(\s*</Score2_TRUE_ANSWER>)", output_str)

    if match1 and match2:

        val1 = int(match1.group(2))
        val2 = int(match2.group(2))
        

        high_score = max(val1, val2)
        low_score = min(val1, val2)
        

        if val1 == high_score:

            tag_with_high_score = match1.group(0)
            tag_to_become_1 = f"{match1.group(1)}2{match1.group(3)}" 
            
            tag_with_low_score = match2.group(0)
            tag_to_become_5 = f"{match2.group(1)}4{match2.group(3)}" 
        else:

            tag_with_high_score = match2.group(0)
            tag_to_become_1 = f"{match2.group(1)}2{match2.group(3)}" 

            tag_with_low_score = match1.group(0)
            tag_to_become_5 = f"{match1.group(1)}4{match1.group(3)}" 

        placeholder_high = "___TEMP_HIGH_SCORE_PLACEHOLDER___"
        output_str = output_str.replace(tag_with_high_score, placeholder_high, 1)
        output_str = output_str.replace(tag_with_low_score, tag_to_become_5, 1)
        output_str = output_str.replace(placeholder_high, tag_to_become_1, 1)


    answer_matches = list(re.finditer(r"(<ANSWER>\s*)(\d+)(\s*</ANSWER>)", output_str))
    
    if len(answer_matches) >= 2:
        match_a = answer_matches[0]
        match_b = answer_matches[1]

        val_a = int(match_a.group(2))
        val_b = int(match_b.group(2))
        
        high_score = max(val_a, val_b)
        low_score = min(val_a, val_b)
        
        if val_a == high_score:
            tag_with_high_score = match_a.group(0)
            tag_to_become_1 = f"{match_a.group(1)}2{match_a.group(3)}"
            
            tag_with_low_score = match_b.group(0)
            tag_to_become_5 = f"{match_b.group(1)}4{match_b.group(3)}"
        else:
            tag_with_high_score = match_b.group(0)
            tag_to_become_1 = f"{match_b.group(1)}2{match_b.group(3)}"
            
            tag_with_low_score = match_a.group(0)
            tag_to_become_5 = f"{match_a.group(1)}4{match_a.group(3)}"

        placeholder_high = "___TEMP_ANSWER_HIGH_PLACEHOLDER___"
        output_str = output_str.replace(tag_with_high_score, placeholder_high, 1)
        output_str = output_str.replace(tag_with_low_score, tag_to_become_5, 1)
        output_str = output_str.replace(placeholder_high, tag_to_become_1, 1)

    return output_str

import random
import re


def randomize_scores_trend_reversal(output_str):
    """
    Randomly modify scores while maintaining consistency and ensuring opposite trend.
    The original "high vs low" is mapped to "low vs high".
    """
    
    if not isinstance(output_str, str):
        return ""
    if not isinstance(output_str, str):
        return ""

    match1 = re.search(r"<Score1_TRUE_ANSWER>\s*(\d+)\s*</Score1_TRUE_ANSWER>", output_str)
    match2 = re.search(r"<Score2_TRUE_ANSWER>\s*(\d+)\s*</Score2_TRUE_ANSWER>", output_str)
    
    if not (match1 and match2):
        return output_str 
        
    val1 = int(match1.group(1))
    val2 = int(match2.group(1))

    if val1 == val2:
        return output_str

    high_score_val = max(val1, val2)
    low_score_val = min(val1, val2)

    new_low = -1
    new_high = -1
    
    while True:
        new_low = random.choice([1, 2, 3, 4])
        possible_highs = [s for s in [2, 3, 4, 5] if s > new_low]
        if not possible_highs:
            new_high = 5
        else:
            new_high = random.choice(possible_highs)

        if not (new_low == low_score_val and new_high == high_score_val):
            break

    score_mapping = {
        high_score_val: new_low,
        low_score_val: new_high
    }

    matches = list(re.finditer(r"(<(Score[12]_TRUE_ANSWER|ANSWER)>\s*)(\d+)(\s*</\2>)", output_str))
    
    for match in reversed(matches):
        prefix = match.group(1)
        original_score_val = int(match.group(3))
        suffix = match.group(4)

        new_score = score_mapping.get(original_score_val, original_score_val)
        new_tag = f"{prefix}{new_score}{suffix}"
        
        start, end = match.span()
        output_str = output_str[:start] + new_tag + output_str[end:]

    return output_str

def swap_scores_in_output(output_str):
    """
    Swap two sets of scores in a string (final version).
    - Swap the scores in the <ANSWER> tag (tag position swap).
    - Swap the numbers in the <Score1_TRUE_ANSWER> and <Score2_TRUE_ANSWER> tags (tag position unchanged).
    """
    answer_matches = list(re.finditer(r"(<ANSWER>\s*\d+\s*</ANSWER>)", output_str))
    
    if len(answer_matches) >= 2:
        original_tag1 = answer_matches[0].group(1)
        original_tag2 = answer_matches[1].group(1)
        
        placeholder = "___TEMP_ANSWER_SWAP_PLACEHOLDER___"
        output_str = output_str.replace(original_tag1, placeholder, 1)
        output_str = output_str.replace(original_tag2, original_tag1, 1)
        output_str = output_str.replace(placeholder, original_tag2, 1)

    match1 = re.search(r"(<Score1_TRUE_ANSWER>\s*)(\d+)(\s*</Score1_TRUE_ANSWER>)", output_str)
    match2 = re.search(r"(<Score2_TRUE_ANSWER>\s*)(\d+)(\s*</Score2_TRUE_ANSWER>)", output_str)

    if match1 and match2:
        prefix1 = match1.group(1) 
        val1 = match1.group(2)     
        suffix1 = match1.group(3)  
        full_tag1 = match1.group(0) 
        
        # For Score2:
        prefix2 = match2.group(1) 
        val2 = match2.group(2)     
        suffix2 = match2.group(3)  
        full_tag2 = match2.group(0) 

        new_tag1_with_val2 = f"{prefix1}{val2}{suffix1}" 
        new_tag2_with_val1 = f"{prefix2}{val1}{suffix2}" 

        placeholder1 = "___TEMP_TRUE_ANSWER_PLACEHOLDER_1___"
        
        output_str = output_str.replace(full_tag1, placeholder1, 1)
        output_str = output_str.replace(full_tag2, new_tag2_with_val1, 1)
        output_str = output_str.replace(placeholder1, new_tag1_with_val2, 1)
        
    return output_str


pe = """
# Goals
# Input
## Story Evaluation Requirements
{instruction}
## Story Analysis Process
{output}
# OutputFormat
[Problem Finding]

[Final judgement]

# Workflow
1、[Problem Finding]: Based on the content of Story Evaluation Requirements and Story Analysis Process, determine whether the story content, story evaluation, and scores are correct and reasonable. For example: if the analysis process emphasizes the shortcomings of the article but the final score is a high one; or if the analysis process considers the article to have many merits but the final score is a low one, then this is unreasonable. If the analysis and scores are consistent and accurate, then it is reasonable.
2、[Final judgement]: Put "Yes" or "No" in <ANSWER></ANSWER>. If there are no issues, answer YES; if it is not logical and there are issues, answer NO.
** Note that the maximum score for the story is 5 points, and the minimum score is 1 point.
** Please objectively evaluate whether the story analysis process and the final scoring are reasonable.
**Start with "# Output\n [Problem Finding] \n\n "** </END>
"""

peList = []
file_path = "../AfterSelfCheck.json"

data = []
try:
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                data.append(json.loads(line))
    print(f"Loaded {len(data)} samples in JSON Lines format")
except json.JSONDecodeError:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} samples in standard JSON format")
    except Exception as e:
        print(f"File loading failed, neither valid JSON nor JSON Lines: {str(e)}")
        exit(1)
except Exception as e:
    print(f"File loading failed: {str(e)}")
    exit(1)

total_samples = len(data)
print(f"Loaded {total_samples} samples for processing")
    
samples_to_process = data

for item in tqdm(samples_to_process, desc="Preparing and modifying input data"):
    instruction = item['instruction']
    original_output = item['output']
    modified_output = randomize_scores_trend_reversal(original_output)
    prompt = pe.format(instruction=instruction, output=modified_output)
    peList.append(prompt)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4, gpu_memory_utilization=0.55)

llm_generated_outputs = llm.generate(peList, sampling_params)

result = []
for i, llm_output in tqdm(enumerate(llm_generated_outputs), total=len(llm_generated_outputs), desc="Processing and merging results"):
    
    original_item = samples_to_process[i]
    self_check_text = llm_output.outputs[0].text
    
    result_item = {
        "instruction": original_item['instruction'],
        "input": "",
        "output": original_item['output'],
        "swapoutput": randomize_scores_trend_reversal(original_item['output']),
        "judge":self_check_text
    }
    result.append(result_item)

with open("../AfterCoTRobustWithJudge.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Processing completed! Saved {len(result)} results")
