import argparse
import os
import json
import datasets

# 严格使用您提供的 instruction 模板
instruction="""
    # Role:
    Story Evaluation Expert

    # Background:
    The user needs to evaluate a given story segment, combined with reviews from the {aspect} perspective.

    # Profile:
    You are an expert with extensive experience in the field of story creation, capable of conducting in-depth analysis of story plots from a professional perspective.

    # Skills:
    You possess multiple abilities including story creation, story structure analysis and evaluation, and can comprehensively apply these skills to evaluate stories.

    # Goals:
    Combining the story content, conduct a detailed evaluation of the story focusing on the {aspect} aspect, and provide an analysis process.

    # Input Section
    ## Story Prompt
    {prompt}
    ## Story Content
    {context}
    ## Evaluation Aspect
    {aspect}

    # OutputFormat:
    【Evaluation and Scoring Process】

    # Workflow:
    1. Output 【Evaluation and Scoring Process】: Provide a detailed analysis process for the existing 【Story Content】 and 【Story Prompt】 focusing on the {aspect} aspect, and ultimately provide a score. You should give me score in <ANSWER> score </ANSWER>
    *Note: There should be a detailed thinking process regarding the story, preferably with specific examples.
    </end>
"""

def main():
    parser = argparse.ArgumentParser(description="Process StoryER JSON data and save as Parquet files.")
    parser.add_argument(
        '--input_dir', 
        default='../HANNA/Data',
        help='Directory containing train.json and test.json files.'
    )
    parser.add_argument(
        '--output_dir', 
        default='../HANNA',
        help='Directory to save the output .parquet files.'
    )
    parser.add_argument('--data-source', default='hanna')
    parser.add_argument('--ability', default='story')
    
    args = parser.parse_args()

    try:
        train_json_path = os.path.join(args.input_dir, 'train.json')
        test_json_path = os.path.join(args.input_dir, 'test.json')
        
        print(f"Loading raw train data from: {train_json_path}")
        raw_dataset = datasets.load_dataset('json', data_files={'train': train_json_path, 'test': test_json_path}, keep_in_memory=True)
    
    except FileNotFoundError as e:
        print(f"Error: {e.filename} not found.")
        return

    train_dataset = raw_dataset['train']
    test_dataset = raw_dataset['test']
    
    print("\nOriginal dataset structure:")
    print(raw_dataset)
    
    data_source = args.data_source
    ability = args.ability

    def make_map_fn(split):
        def process_fn(example, idx):
            context = example.get('context', '')
            aspect = example.get('aspect', '')
            answer = example.get('score')
            pe = example.get('prompt', '')
            prompt = instruction.format(context=context, aspect=aspect, prompt=pe)
            
            
            # 返回一个只包含新字段的字典
            return {
                "data_source": data_source,
                "prompt": [{
                    "role": "user",
                    "content": prompt,
                }],
                "ability": ability,
                "reward_model": {
                    "style": "rule",
                    "ground_truth": answer
                },
                "extra_info": {
                    'split': split,
                    'index': idx,
                    'answer': answer,
                    "question": prompt,
                }
            }
        return process_fn

    print("\nProcessing dataset...")
    

    train_dataset_mapped = train_dataset.map(
        function=make_map_fn('train'), 
        with_indices=True,
        num_proc=8
    )
    test_dataset_mapped = test_dataset.map(
        function=make_map_fn('test'), 
        with_indices=True,
        num_proc=8
    )

    train_dataset_filtered = train_dataset_mapped.filter(
        lambda example: example["data_source"] is not None,
        num_proc=8
    )
    test_dataset_filtered = test_dataset_mapped.filter(
        lambda example: example["data_source"] is not None,
        num_proc=8
    )

    final_columns = ["data_source", "prompt", "ability", "reward_model", "extra_info"]
    train_dataset_processed = train_dataset_filtered.select_columns(final_columns)
    test_dataset_processed = test_dataset_filtered.select_columns(final_columns)


    print("\nProcessed dataset structure:")
    print(train_dataset_processed)
    print("\nProcessed first training data:")
    print(json.dumps(train_dataset_processed[0], indent=2, ensure_ascii=False))

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    train_output_path = os.path.join(output_dir, 'train.parquet')
    test_output_path = os.path.join(output_dir, 'test.parquet')

    print(f"\nSaving processed training set to: {train_output_path}")
    train_dataset_processed.to_parquet(train_output_path)
    
    print(f"Saving processed test set to: {test_output_path}")
    test_dataset_processed.to_parquet(test_output_path)
    
    print("\nProcessing completed!")

if __name__ == '__main__':
    main()
