import re
import math
import os
from openai import OpenAI 

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



from vllm import LLM, SamplingParams
import json 


import re
import math
from openai import AsyncOpenAI 

ASPECTS_AND_WEIGHTS = {
    'Relevance': 5,
    'Coherence': 3,
    'Empathy': 1,
    'Surprise': 3,
    'Engagement': 1,
    'Complexity': 1
}


ASPECT_TO_API_BASE = {
    'Relevance': "vllm-api-relevance",
    'Coherence': "vllm-api-coherence",
    'Empathy': "vllm-api-empathy",
    'Surprise': "vllm-api-surprise",
    'Engagement': "vllm-api-engagement",
    'Complexity': "vllm-api-complexity"
}


def compute_score(data_source, solution_str, ground_truth, extra_info) -> float:
    """
    """
    print("--- Synchronous wrapper called, starting parallel asynchronous evaluation ---")
    try:
        final_score = asyncio.run(
            compute_score_parallel(data_source, solution_str, ground_truth, extra_info)
        )
        return final_score
    except Exception as e:
        print(f"Error in asynchronous evaluation: {e}")
        return 0.0


def transform_difference(score_diff, max_diff=4.0, k=2.0):
    if max_diff == 0: return 0.0
    normalized_diff = score_diff / max_diff
    return math.copysign(abs(normalized_diff) ** k, normalized_diff)

async def evaluate_aspect_async(aspect, api_base_url, model_path, instruction):

    openai_api_key = "openai_api_key"
    
    try:
        async with AsyncOpenAI(api_key=openai_api_key, base_url=api_base_url) as client:
            response = await client.completions.create(
                model=model_path,
                prompt=instruction,
                max_tokens=1000
            )
            eva_context = response.choices[0].text
            
            answer_pattern = r'<ANSWER>(.*?)(\d+)'
            matches = re.finditer(answer_pattern, eva_context, re.DOTALL)
            answer_values = [int(match.group(2)) for match in matches]
            
            if len(answer_values) >= 2:
                print(f"  <- [Success] Dimension: '{aspect}'")
                return aspect, answer_values[0], answer_values[1]
            else:
                print(f"  <- [Warning] Dimension: '{aspect}' failed to parse paired scores.")
                return aspect, 0, 0

    except Exception as e:
        print(f"  <- [Failed] Dimension: '{aspect}' (Target: {api_base_url}) Error: {e}")
        return aspect, 0, 0


async def compute_score_parallel(data_source, solution_str, ground_truth, extra_info) -> float:
    """
    """
    prompt = extra_info['prompt']
    model_path = "../model_name" 

    print("\n--- Start parallel multi-dimensional evaluation (LLM scoring range: 1-5) ---")
    
    tasks = []
    for aspect in ASPECTS_AND_WEIGHTS.keys():
        current_api_base = ASPECT_TO_API_BASE.get(aspect, "vllm-api-relevance")
        instruction_ = instruction.format(
            aspect=aspect,
            context1=solution_str, 
            context2=ground_truth, 
            prompt1=prompt, 
            prompt2=prompt
        )
        task = asyncio.create_task(evaluate_aspect_async(aspect, current_api_base, model_path, instruction_))
        tasks.append(task)
        
    results = await asyncio.gather(*tasks)
    
    print("\n--- All parallel evaluations completed, starting result processing ---")

    solution_scores = {}
    ground_truth_scores = {}
    for aspect_result, sol_score, gt_score in results:
        solution_scores[aspect_result] = sol_score
        ground_truth_scores[aspect_result] = gt_score

    total_weight = sum(ASPECTS_AND_WEIGHTS.values())
    if total_weight == 0: return 0.0
        
    
    avg_solution_score = sum(solution_scores.get(aspect, 0) * weight for aspect, weight in ASPECTS_AND_WEIGHTS.items()) / total_weight
    avg_gt_score = sum(ground_truth_scores.get(aspect, 0) * weight for aspect, weight in ASPECTS_AND_WEIGHTS.items()) / total_weight
    
    absolute_reward = (avg_solution_score - 1) / 4
    absolute_reward = max(0, min(1, absolute_reward))  
    
    score_difference = avg_solution_score - avg_gt_score  

    if score_difference <= 0:
        relative_reward = 0.2 / (1 + math.exp(-10 * (score_difference + 0.1)))
    else:
        relative_reward = 1 - math.exp(-score_difference)

    
    relative_reward = max(0, min(1, relative_reward))  
    
    solution_length = len(solution_str)
    min_ideal_length, max_ideal_length = 800, 1200
    
    if solution_length < min_ideal_length:
        length_reward = solution_length / min_ideal_length
    elif solution_length > max_ideal_length:
        excess_length = solution_length - max_ideal_length
        length_reward = 0.7 + 0.3 * math.exp(-excess_length / 500)
    else:
        length_reward = 1.0
    
    length_reward = max(0, min(1, length_reward))  
    
    total_reward = (0.1 * absolute_reward + 
                   0.8 * relative_reward + 
                   0.1 * length_reward)
    
    print("\n--- Reward function detailed calculation ---")
    print(f"Solution average score: {avg_solution_score:.2f}/5.0")
    print(f"Ground Truth average score: {avg_gt_score:.2f}/5.0")
    print(f"Score difference: {score_difference:+.2f}")
    print(f"")
    print(f"1. Absolute reward (20%): {absolute_reward:.4f}")
    print(f"   - Original score: {avg_solution_score:.2f} → Reward: {absolute_reward:.4f}")
    print(f"")
    print(f"2. Relative reward (60%): {relative_reward:.4f}")
    print(f"   - Score difference: {score_difference:+.2f} → Reward: {relative_reward:.4f}")
    print(f"")
    print(f"3. Length reward (20%): {length_reward:.4f}")
    print(f"   - Text length: {solution_length} characters")
    print(f"")
    print(f"==> Total reward: {total_reward:.4f}")
    
    return round(total_reward, 4)
