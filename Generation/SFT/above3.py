instruction_template="""
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
import pandas as pd
from sklearn.model_selection import train_test_split
import json
import os

csv_path = '../HANNA/hanna_stories_annotations.csv'
output_dir = "../HANNA/Data/above3"

prompt_story_columns = ['Prompt', 'Story']
score_columns = ['Relevance', 'Coherence', 'Empathy', 'Surprise', 'Engagement', 'Complexity']
SCORE_THRESHOLD = 3

TRAIN_RATIO = 0.8
VAL_RATIO = 0.1
TEST_RATIO = 0.1
RANDOM_STATE = 42

print("--- 1. Reading CSV file and preprocessing data ---")
df = pd.read_csv(csv_path)

grouped = []
for i in range(0, len(df), 3):
    group_data = df.iloc[i:i + 3]
    prompt_story_info = group_data[prompt_story_columns].iloc[0]
    score_means = group_data[score_columns].mean()
    overall_average_score = score_means.mean()
    
    combined = {
        **prompt_story_info.to_dict(),
        **score_means.to_dict(),
        'Overall_Average_Score': overall_average_score
    }
    grouped.append(combined)

result_df = pd.DataFrame(grouped)
print(f"After grouping and aggregation, there are {len(result_df)} independent Prompt-Story data.")

print("\n--- 2. Splitting dataset by Prompt to prevent data leakage ---")
unique_prompts = result_df['Prompt'].unique()
print(f"There are {len(result_df)} items in the dataset, based on {len(unique_prompts)} unique Prompts.")

train_prompts, temp_prompts = train_test_split(
    unique_prompts,
    test_size=(VAL_RATIO + TEST_RATIO),
    random_state=RANDOM_STATE,
    shuffle=True
)

val_prompts, test_prompts = train_test_split(
    temp_prompts,
    test_size=(TEST_RATIO / (VAL_RATIO + TEST_RATIO)),
    random_state=RANDOM_STATE,
    shuffle=True
)

print(f"\nPrompt split results:")
print(f"Training set Prompts: {len(train_prompts)}")
print(f"Validation set Prompts: {len(val_prompts)}")
print(f"Test set Prompts: {len(test_prompts)}")

train_df = result_df[result_df['Prompt'].isin(train_prompts)]
val_df = result_df[result_df['Prompt'].isin(val_prompts)]
test_df = result_df[result_df['Prompt'].isin(test_prompts)]

print(f"\n--- 3. Filtering training set by score (Overall_Average_Score > {SCORE_THRESHOLD}) ---")
initial_train_count = len(train_df)
train_df_filtered = train_df[train_df['Overall_Average_Score'] > SCORE_THRESHOLD]
print(f"Training set initial data: {initial_train_count} items")
print(f"Filtered training set data: {len(train_df_filtered)} items (filtered out {initial_train_count - len(train_df_filtered)} items)")

def format_data(df_to_format, template_instruction):
    data_list = []
    for _, row in df_to_format.iterrows():
        instruction_ = template_instruction.format(prompt=row['Prompt'])
        output_text = row['Story']
        item = {
            "instruction": instruction_,
            "input": "",
            "output": f"# Output \n 【Story Content】\n {output_text}"
        }
        data_list.append(item)
    return data_list

train_data = format_data(train_df_filtered, instruction_template)
val_data = format_data(val_df, instruction_template)
test_data = format_data(test_df, instruction_template)

result = train_data + val_data + test_data

print("\n--- 4. Saving dataset to JSON file ---")
os.makedirs(output_dir, exist_ok=True)

def save_to_json(data, path):
    if not data:
        print(f"Warning: Dataset '{path}' is empty, no file will be created.")
        return
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Dataset successfully saved to file: {path}")

save_to_json(train_data, os.path.join(output_dir, "train.json"))
save_to_json(val_data, os.path.join(output_dir, "val.json"))
save_to_json(test_data, os.path.join(output_dir, "test.json"))

print("\n--- 5. Printing dataset statistics ---")
print(f"Total data (excluding discarded parts due to score filtering): {len(result)} items")
print(f"Training set: {len(train_data)} items ({len(train_data)/len(result)*100:.1f}%)")
print(f"Validation set: {len(val_data)} items ({len(val_data)/len(result)*100:.1f}%)")
print(f"Test set: {len(test_data)} items ({len(test_data)/len(result)*100:.1f}%)")
print(f"Since grouped by Prompt and the training set was filtered by score, the actual ratio may deviate slightly from {TRAIN_RATIO*100}:{VAL_RATIO*100}:{TEST_RATIO*100}, which is normal.")

print("\n--- 6. Verifying if Prompts are independent in each dataset ---")
train_instructions = {item['instruction'] for item in train_data}
val_instructions = {item['instruction'] for item in val_data}
test_instructions = {item['instruction'] for item in test_data}

assert len(train_instructions.intersection(val_instructions)) == 0, "Error: Training set and validation set have overlapping Instructions!"
assert len(train_instructions.intersection(test_instructions)) == 0, "Error: Training set and test set have overlapping Instructions!"
assert len(val_instructions.intersection(test_instructions)) == 0, "Error: Validation set and test set have overlapping Instructions!"

print("Verification successful: All Instructions are completely independent in training, validation, and test sets, with no overlap.")

print("\n--- 7. Saving dataset basic information ---")
dataset_info = {
    "total_samples_after_split_and_filter": len(result),
    "train_samples": len(train_data),
    "val_samples": len(val_data),
    "test_samples": len(test_data),
    "train_ratio": len(train_data) / len(result) if len(result) > 0 else 0,
    "val_ratio": len(val_data) / len(result) if len(result) > 0 else 0,
    "test_ratio": len(test_data) / len(result) if len(result) > 0 else 0,
    "split_strategy": "Grouped by unique Prompt to prevent data leakage, then filtered train set by score",
    "score_filter_threshold": SCORE_THRESHOLD,
    "unique_prompts_total": len(unique_prompts),
    "unique_prompts_train": len(train_prompts),
    "unique_prompts_val": len(val_prompts),
    "unique_prompts_test": len(test_prompts),
    "random_state": RANDOM_STATE,
    "instruction_template": instruction_template
}

info_path = os.path.join(output_dir, "dataset_info.json")
with open(info_path, "w", encoding="utf-8") as f:
    json.dump(dataset_info, f, ensure_ascii=False, indent=2)
print(f"Dataset information saved to: {info_path}")

