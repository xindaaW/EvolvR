import json
import re
import os

def load_json_data(file_path):
    """
    Smartly load JSON files.
    Can handle two formats:
    1. A large JSON array: [{}, {}, ...]
    2. JSON Lines format: One JSON object per line
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print("Failed to parse as standard JSON array, trying JSON Lines format (one object per line)...")
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    try:
                        data.append(json.loads(line))
                    except json.JSONDecodeError:
                        print(f"Warning: Found unparsable line, skipping: {line.strip()}")
        return data

def filter_and_clean_data(data, debug_mode=False, debug_item_limit=10):
    """
    Filter data, check the consistency of the output field, and clean the data that passes the check.

    Args:
        data (list): A list containing JSON objects.
        debug_mode (bool): Whether to enable debug mode, print detailed process.
        debug_item_limit (int): Maximum number of items to process in debug mode.

    Returns:
        tuple: (Valid and cleaned JSON object list, total number of processed items)
    """
    valid_and_cleaned_objects = []
    total_count = len(data)
    items_to_process = data

    if debug_mode:
        print(f"--- Enable debug mode, will check and clean the first {debug_item_limit} items ---")
        items_to_process = data[:debug_item_limit]

    for i, item in enumerate(items_to_process):
        is_match = False
        reason = ""

        if debug_mode:
            print(f"\n--- [Checking the {i+1}th item] ---")

        output_text = item.get('output', '')
        
        answers = re.findall(r'<ANSWER>(.*?)</ANSWER>', output_text, re.DOTALL)
        score1_match = re.search(r'<Score1_TRUE_ANSWER>(.*?)</Score1_TRUE_ANSWER>', output_text, re.DOTALL)
        score2_match = re.search(r'<Score2_TRUE_ANSWER>(.*?)</Score2_TRUE_ANSWER>', output_text, re.DOTALL)
        
        if len(answers) != 2:
            reason = f"Found {len(answers)} <ANSWER> tags, need 2."
        elif not score1_match:
            reason = "No <Score1_TRUE_ANSWER> tag found."
        elif not score2_match:
            reason = "No <Score2_TRUE_ANSWER> tag found."
        else:
            # Clean extracted data (remove leading and trailing spaces) for comparison
            answer1 = answers[0].strip()
            answer2 = answers[1].strip()
            true_score1 = score1_match.group(1).strip()
            true_score2 = score2_match.group(1).strip()
            
            if debug_mode:
                print(f"  Extracted <ANSWER>: ['{answer1}', '{answer2}'] (removed spaces)")
                print(f"  Extracted <Score1_TRUE_ANSWER>: '{true_score1}' (removed spaces)")
                print(f"  Extracted <Score2_TRUE_ANSWER>: '{true_score2}' (removed spaces)")
            
            if answer1 == true_score1 and answer2 == true_score2:
                is_match = True
                reason = "All values matched successfully."
            else:
                reason = f"Values do not match: Answer1('{answer1}') vs Score1('{true_score1}'), Answer2('{answer2}') vs Score2('{true_score2}')"
        
        if is_match:
            # Cleaned output: only clean data that matches
            cleaned_output = output_text
            
            # Use re.sub to clean spaces inside <ANSWER> tags
            # 模式解释: (<ANSWER>)(\s*)(.*?)(\s*)(</ANSWER>)
            # \1: <ANSWER>
            # \2: leading spaces
            # \3: content
            # \4: trailing spaces
            # \5: </ANSWER>
            # Replace with: \1\3\5  (i.e., tag+content+tag, removing spaces in the middle)
            cleaned_output = re.sub(r'(<ANSWER>)\s*(.*?)\s*(</ANSWER>)', r'\1\2\3', cleaned_output)
            cleaned_output = re.sub(r'(<Score1_TRUE_ANSWER>)\s*(.*?)\s*(</Score1_TRUE_ANSWER>)', r'\1\2\3', cleaned_output)
            cleaned_output = re.sub(r'(<Score2_TRUE_ANSWER>)\s*(.*?)\s*(</Score2_TRUE_ANSWER>)', r'\1\2\3', cleaned_output)

            # Create a new dictionary to store modified data
            cleaned_item = item.copy()
            cleaned_item['output'] = cleaned_output
            valid_and_cleaned_objects.append(cleaned_item)
            
            if debug_mode:
                print(f"  [Result]: ✅ Keep and clean. Reason: {reason}")
        else:
            if debug_mode:
                print(f"  [Result]: ❌ Discard. Reason: {reason}")
    
    if debug_mode:
        print("\n--- Debug mode completed ---")

    return valid_and_cleaned_objects, total_count



if __name__ == '__main__':

    DEBUG_MODE = False 

    ITEMS_TO_DEBUG = 10

    input_file = "../Multi_persona_Pairwise_7B_CoT_HANNA.json"
    output_file = "../MultiPersonaAfterRuleCheck.json"

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist. Please check the file name and path.")
    else:
        all_data = load_json_data(input_file)
        
        if all_data:
            filtered_data, total_items = filter_and_clean_data(all_data, DEBUG_MODE, ITEMS_TO_DEBUG)
            
            with open(output_file, 'w', encoding='utf-8') as f_out:
                for obj in filtered_data:
                    f_out.write(json.dumps(obj, ensure_ascii=False) + '\n')

            print("\n================== Summary ==================")
            if DEBUG_MODE:
                print(f"In debug mode, checked {min(total_items, ITEMS_TO_DEBUG)} items.")
            else:
                print(f"In full mode, processed {total_items} items.")
            
            print(f"Kept {len(filtered_data)} matching items and cleaned their 'output' field.")
            
            if not DEBUG_MODE:
                 discarded_count = total_items - len(filtered_data)
                 print(f"Discarded {discarded_count} items that did not match or had formatting errors.")
            
            print(f"Final results saved to: {output_file}")
            print("==========================================")
