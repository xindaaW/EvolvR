instruction="""
# Role:
Story Evaluation Expert

# Background:
The user needs to evaluate given story segments based on story prompts from the {aspect} perspective.

# Profile:
You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

# Skills:
You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

# Goals:
Combining the two writing requirements and story contents, conduct detailed evaluations of both stories focusing on {aspect}, provide separate analysis processes, and note that since the two stories have different scores, you need to compare the contents of both and provide an analysis process.

# Input Section
## Evaluation Aspect
{aspect}
## Writing Requirement 1
{prompt1}
## Story Content 1
{context1}
## Writing Requirement 2
{prompt2}
## Story Content 2
{context2}

# OutputFormat:
【Content Analysis】
【Evaluation and Scoring Process】

# Workflow:
1. Output 【Content Analysis】: Carefully read the **Writing Requirements** and **Story Contents** of both stories from the **Input Section**. Understand the **Story Contents** from a professional perspective. Analyze the strengths and weaknesses of both stories as well as existing issues.
2. Output 【Evaluation and Scoring Process】: Based on the two 【Story Contents】, provide a detailed analysis process. **Note**: The maximum score is 5 points. Ultimately provide specific scores with reasoning for each. You should give me scores in <ANSWER> score1 </ANSWER> | <ANSWER> score2 </ANSWER>
*Note: There should be detailed thinking processes for both stories, preferably with specific examples.
</end>
"""

autoj_instruction = """
You are assessing two submitted responses on a given user's query and judging which response is better or they are tied. Here is the data:

[BEGIN DATA]
***
[Query]: {prompt}
***
[Response 1]: {response}
***
[Response 2]: {response_another}
***
[END DATA]

Here are the instructions to assess and compare the two responses:

1. Pinpoint the key factors to distinguish these two responses.
2. Conclude your comparison by providing a final decision on which response is better, or they are tied. Begin your final decision statement with "So, the final decision is Response 1 / Response 2 / Tie". Ensure that your decision aligns coherently with the comprehensive evaluation and comparison you've provided."""

from vllm import LLM, SamplingParams
import json 

pe = []
file_path = "../HANNA/Data/PairTest/random4_pairs.json"  


with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    if not data or not isinstance(data[0], dict):
        print("Data format does not meet expectations, please check JSON file structure")
        exit(1)
        
    total_samples = len(data)
    print(f"Loaded {total_samples} samples")
    
    for sample in data:
        context1 = sample["context1"]
        context2 = sample["context2"]
        aspect = sample["aspect"]
        score1 = sample["score1"]
        prompt1= sample["prompt1"]
        score2 = sample["score2"]
        prompt2= sample["prompt2"]
        instruction_ = instruction.format(context1=context1, context2=context2, aspect=aspect, prompt1=prompt1, prompt2=prompt2)
        # instruction_ = autoj_instruction.format()
        pe.append(instruction_)

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4, gpu_memory_utilization=0.8)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    instruction_ = instruction.format(context1=item['context1'], context2=item['context2'], aspect=item['aspect'], prompt1=prompt1, prompt2=prompt2)

    result_item = {
        "instruction": instruction_,
        "output": generated_text,
        "final score 1": item['score1'],
        "final score 2": item['score2']
    }
    result.append(result_item)
    
with open("../MultiPersona_random4_epoch_10000.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")