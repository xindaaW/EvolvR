instruction="""
# Role:
Story Evaluation Expert

# Background:
The user requires an evaluation of given story segments from the {aspect} perspective, combined with commentary.

# Profile:
You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional standpoint.

# Skills:
You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

# Goals:
Considering the content of two stories, conduct a detailed evaluation of both stories regarding the {aspect}, providing separate analysis processes for each. You need to compare the content of both and provide an analytical process.

# Input Section
## Evaluation Aspect
{aspect}

## Story Content 1
{context1}

## Story Content 2
{context2}

# OutputFormat:
[Content Analysis]
[Evaluation and Scoring Process]

# Workflow:
1. Output [Content Analysis]: Carefully read the **Story Content** of both stories in the **Input Section**, understanding the **Story Content** from a professional perspective. Analyze the strengths, weaknesses, and existing issues in both stories.
2. Output [Evaluation and Scoring Process]: Based on the content of both stories, provide a detailed analysis process. **Note**: The maximum score is 5 points. You must ultimately provide specific scores and reasoning for each. You should give me scores in the format: <ANSWER> score1 </ANSWER> | <ANSWER> score2 </ANSWER>
*Note: You need to have a detailed thinking process and comparison process for both stories, preferably with specific examples.
</end>
"""
from vllm import LLM, SamplingParams
import json 

pe = []
file_path = "../StoryER/Data/output/point/test.json"

origin_text = None

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    if not data or not isinstance(data[0], dict):
        print("Data format does not meet expectations, please check JSON file structure")
        exit(1)
        
    print(f"Loaded {len(data)} samples")
    
    for i, sample in enumerate(data):
        context1 = sample["context"]
        aspect1 = sample["aspect"]
        score1 = sample["score"]
        comment1 = sample["comment"]
        
        if i == 0:
            origin_text = context1
            
        instruction_ = instruction.format(context1=context1, context2=origin_text, aspect=aspect1)
        pe.append(instruction_)

if origin_text:
    print(f"First sample's context has been saved to origin_text variable, length: {len(origin_text)}")
else:
    print("No valid samples")

sampling_params = SamplingParams(temperature=1, top_p=0.95, max_tokens=1000, repetition_penalty=1)
llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4, gpu_memory_utilization=0.8)
outputs = llm.generate(pe, sampling_params)

result = []
for output, item in zip(outputs, data):
    prompt = output.prompt
    generated_text = output.outputs[0].text
    instruction_ = instruction.format(context1=item['context'], context2=origin_text, aspect=item['aspect'])

    result_item = {
        "instruction": instruction_,
        "output": generated_text,
        "final score 1": item['score']
    }
    result.append(result_item)

with open("../7B_Pair_test_second_origin.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f"Saved {len(result)} processed results")