import json
from vllm import LLM, SamplingParams

instruction="""
    # Role:
    Story Creation Expert
    # Background:
    The user needs to complete story creation based on creative requirements.
    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of writing stories with excellent relevance, coherence, empathy, surprise, engagement, and complexity using professional techniques.
    # Skills:
    You possess multiple abilities including story creation and story structure analysis, and can comprehensively apply these skills for story writing.
    # Goals:
    Based on the creative requirements, write story works with excellent relevance, coherence, empathy, surprise, engagement, and complexity.
    # Input Section
    ## Creative Requirements
    {prompt}
    # OutputFormat:
    【Story Content】
    # Workflow:
    1. Output 【Story Content】: Based on the creative requirements, write story works with excellent relevance, coherence, empathy, surprise, engagement, and complexity.
    ● Relevance: Refers to the degree of correlation and fit between content and themes, requirements, etc.
    ● Coherence: Reflects the smoothness and consistency of content logic, structure, and other aspects
    ● Empathy: Emphasizes understanding and resonance with others' emotions and situations
    ● Surprise: Relates to the degree of unexpected and novel feelings brought by the content
    ● Engagement: Indicates the degree of audience involvement and interaction
    ● Complexity: Reflects the complexity of content in terms of structure, connotation, and other aspects, commonly used to measure the depth and richness of content, such as plot complexity of stories, professional complexity of knowledge content, etc.
    Mark the end of the story with </END>.
"""

file_path = "../HANNA/Data/test.json"
with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Original data has {len(data)} items, sampling at 1/6 ratio...")
prompts = []
source_items = []  
i = 0
for item in data:
    if i % 6 == 0:
        pe = instruction.format(prompt=item['prompt'])
        prompts.append(pe)
        source_items.append(item)  
    i += 1
print(f"After sampling, {len(prompts)} prompts to generate.")


sampling_params = SamplingParams(
    temperature=1, 
    top_p=0.95,
    max_tokens=2048,  
    repetition_penalty=1
)

llm = LLM(model="../Qwen2.5-7B-Instruct", tensor_parallel_size=4, gpu_memory_utilization=0.8)

print("\nStarting generation...")
outputs = llm.generate(prompts, sampling_params)

results = []
for output, item in zip(outputs, source_items):
    raw_generated_text = output.outputs[0].text
    
    cleaned_text = raw_generated_text.split('</END>')[0].strip()
    result = {
        "prompt": item['prompt'],   
        "context": cleaned_text    
    }
    results.append(result)
    
output_file = "../StoryGeneration/Data/test.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nGeneration completed! Generated {len(results)} results")
print(f"Results saved to: {output_file}")