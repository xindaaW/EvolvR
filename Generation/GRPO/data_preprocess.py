import argparse
import os
import json
import datasets

def main():
    parser = argparse.ArgumentParser(description="Process StoryER JSON data and save as Parquet files.")
    parser.add_argument(
        '--input_dir', 
        default='../StoryGeneration/Data_grpo_hanna',
        help='Directory containing train.json and test.json files.'
    )
    parser.add_argument(
        '--output_dir', 
        default='../HANNA_Story_Generation_v2_hanna',
        help='Directory to save the output .parquet files.'
    )
    parser.add_argument('--data-source', default='hanna-story-generation-pair')
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
            prompt = example.get('instruction', '')

            answer = example.get('output', '')
            # aspect = example.get('aspect', '')
            # score = example.get('score')

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
                    "prompt": prompt,
                    # "aspect": aspect,
                    # "score": score
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
