import json
import os
import vllm
from tqdm import tqdm
import re


MODEL_PATH = "../Qwen2.5-7B-Instruct" 
TENSOR_PARALLEL_SIZE = 4
INPUT_FILE = "../AfterCoTRobust.json"
OUTPUT_FILE = "../LogitAnalysis.json"
DEBUG_MODE = False
ITEMS_TO_DEBUG = 5
SCORE_CHOICES = ['1', '2', '3', '4', '5']

def load_json_lines(file_path):

    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    data.append(json.loads(line))
        print(f"Loaded {len(data)} samples")
    except json.JSONDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Loaded {len(data)} samples")
        except Exception as e:
            print(f"File loading failed, neither valid JSON nor JSON Lines: {str(e)}")
            exit(1)
    except Exception as e:
        print(f"File loading failed: {str(e)}")
        exit(1)
    return data

def construct_prompts_from_item(item, i):
    """

    """
    instruction = item.get('instruction', '')
    output_text = item.get('output') 


    if not output_text or not isinstance(output_text, str):
        print(f"Warning: The 'output' field of the {i+1}th data is invalid (None, empty, or non-string). Skipped.")
        return None, None


    analysis_marker = "【Content Analysis】"
    analysis_start_pos = output_text.find(analysis_marker)
    

    if analysis_start_pos == -1:
        search_base_text, search_offset = output_text, 0
    else:
        search_base_text = output_text[analysis_start_pos:]
        search_offset = analysis_start_pos


    try:
        score1_match = re.search(r'<Score1_TRUE_ANSWER>\s*(\d+)\s*</Score1_TRUE_ANSWER>', output_text)
        score2_match = re.search(r'<Score2_TRUE_ANSWER>\s*(\d+)\s*</Score2_TRUE_ANSWER>', output_text)
        if not score1_match or not score2_match:
            raise ValueError("Cannot extract <Score1_TRUE_ANSWER> or <Score2_TRUE_ANSWER>")
        true_score1, true_score2 = score1_match.group(1).strip(), score2_match.group(1).strip()
    except Exception as e:
        print(f"Warning: The {i+1}th data parsing true score failed: {e}. Skipped.")
        return None, None


    prompts, metadata = [], []
    pos1_start_relative = search_base_text.find('<ANSWER>')
    if pos1_start_relative != -1:
        pos1_start_abs = search_offset + pos1_start_relative
        prompts.append(instruction + output_text[:pos1_start_abs + len('<ANSWER>')])
        metadata.append({'original_index': i, 'score_index': 1, 'true_score': true_score1})


    pos2_start_relative = search_base_text.find('<ANSWER>', pos1_start_relative + len('<ANSWER>'))
    if pos2_start_relative != -1:
        pos2_start_abs = search_offset + pos2_start_relative
        prompts.append(instruction + output_text[:pos2_start_abs + len('<ANSWER>')])
        metadata.append({'original_index': i, 'score_index': 2, 'true_score': true_score2})
        
    return prompts, metadata

def main():
    print("Loading VLLM model...")
    llm = vllm.LLM(model=MODEL_PATH, tensor_parallel_size=TENSOR_PARALLEL_SIZE)
    tokenizer = llm.get_tokenizer()
    print("Model loaded successfully!")

    score_to_token_id = {}
    print(f"Mapping scores {SCORE_CHOICES} to token IDs...")
    for score in SCORE_CHOICES:
        token_ids = tokenizer.encode(score, add_special_tokens=False)
        if len(token_ids) == 1:
            score_to_token_id[score] = token_ids[0]
        else:
            print(f"Warning: The score '{score}' is encoded as multiple tokens: {token_ids}. Using the first token ID.")
            score_to_token_id[score] = token_ids[0] if token_ids else -1
    print(f"Score to Token ID mapping: {score_to_token_id}")

    print(f"Loading data from '{INPUT_FILE}'...")
    all_data = load_json_lines(INPUT_FILE)
    if DEBUG_MODE:
        all_data = all_data[:ITEMS_TO_DEBUG]

    all_prompts, all_metadata = [], []
    print("Constructing inference tasks...")
    for i, item in enumerate(tqdm(all_data, desc="Constructing Prompts")):
        prompts, metadata = construct_prompts_from_item(item, i)

        if prompts and metadata:
            all_prompts.extend(prompts)
            all_metadata.extend(metadata) 

    if not all_prompts:
        print("Failed to construct any valid inference tasks, program terminated.")
        return

    sampling_params = vllm.SamplingParams(temperature=0, max_tokens=1, logprobs=20)

    print(f"Starting batch inference with VLLM for {len(all_prompts)} tasks...")
    outputs = llm.generate(all_prompts, sampling_params)
    print("Inference completed!")

    print("Analyzing logits and generating reports...")
    analysis_results = [{} for _ in all_data]

    for i, output in enumerate(tqdm(outputs, desc="Analyzing results")):
        meta = all_metadata[i]
        original_item_index = meta['original_index']
        
        if 'original_data' not in analysis_results[original_item_index]:
            analysis_results[original_item_index]['original_data'] = all_data[original_item_index]
            analysis_results[original_item_index]['checks'] = []

        logprob_dict = output.outputs[0].logprobs[0]
        true_score_str = meta['true_score']
        
        logits_for_choices = {}
        for score, token_id in score_to_token_id.items():
            if token_id in logprob_dict:
                logits_for_choices[score] = round(logprob_dict[token_id].logprob, 4)
            else:
                logits_for_choices[score] = -float('inf')

        best_choice_predicted = max(logits_for_choices, key=logits_for_choices.get) if logits_for_choices else "N/A"
        
        is_highest_among_choices = (true_score_str == best_choice_predicted)

        absolute_highest_token_id = max(logprob_dict, key=lambda tid: logprob_dict[tid].logprob)
        true_score_token_id = score_to_token_id.get(true_score_str, -1)
        is_absolute_highest_logit = (absolute_highest_token_id == true_score_token_id)

        check_detail = {
            f"score{meta['score_index']}_check": {
                "prompt_used_preview": output.prompt[-200:],
                "true_score": true_score_str,
                "is_absolute_highest_logit": is_absolute_highest_logit,
                "is_highest_among_choices": is_highest_among_choices,
                "best_choice_predicted": best_choice_predicted,
                "logits_for_choices": logits_for_choices
            }
        }
        analysis_results[original_item_index]['checks'].append(check_detail)

    print(f"Saving detailed analysis reports to '{OUTPUT_FILE}'...")
    final_results = [res for res in analysis_results if res]
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_results, f, indent=2, ensure_ascii=False)
    
    match_count_new = sum(1 for res in final_results for check in res.get('checks', []) for detail in check.values() if detail.get('is_highest_among_choices'))
    total_checks = len(all_prompts)
    
    print("\n================== Summary ==================")
    print(f"Total analyzed {len(final_results)} valid original data.")
    print(f"Total logits checks: {total_checks}")
    print(f"Number of successful matches based on new standard (highest in {SCORE_CHOICES}): {match_count_new}")
    if total_checks > 0:
        accuracy = (match_count_new / total_checks) * 100
    print(f"Accuracy: {accuracy:.2f}%")
    print(f"Detailed reports saved to: {OUTPUT_FILE}")
    print("==========================================")


if __name__ == '__main__':
    main()
