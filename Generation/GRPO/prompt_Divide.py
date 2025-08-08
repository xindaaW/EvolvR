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

import pandas as pd
from sklearn.model_selection import train_test_split
import json
import os

df = pd.read_csv('../StoryGeneration/hanna_stories_annotations.csv')
prompt_story_columns = ['Prompt', 'Story']
score_columns = ['Relevance', 'Coherence', 'Empathy', 'Surprise', 'Engagement', 'Complexity']

grouped = []
for i in range(0, len(df), 3):
    group_data = df.iloc[i:i + 3]
    prompt_story_info = group_data[prompt_story_columns].iloc[0]
    score_means = group_data[score_columns].mean()
    combined = {**prompt_story_info.to_dict(), **score_means.to_dict()}
    grouped.append(combined)

result_df = pd.DataFrame(grouped)

unique_prompts = result_df['Prompt'].unique()
print(f"There are {len(result_df)} items in the dataset, based on {len(unique_prompts)} unique Prompts.")

train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1

train_prompts, temp_prompts = train_test_split(
    unique_prompts,
    test_size=(val_ratio + test_ratio),
    random_state=42,
    shuffle=True
)

val_prompts, test_prompts = train_test_split(
    temp_prompts,
    test_size=(test_ratio / (val_ratio + test_ratio)),
    random_state=42,
    shuffle=True
)

print(f"\nPrompt split results:")
print(f"Training set Prompts: {len(train_prompts)}")
print(f"Validation set Prompts: {len(val_prompts)}")
print(f"Test set Prompts: {len(test_prompts)}")


train_df = result_df[result_df['Prompt'].isin(train_prompts)]
val_df = result_df[result_df['Prompt'].isin(val_prompts)]
test_df = result_df[result_df['Prompt'].isin(test_prompts)]

def format_data(df):
    data_list = []
    for _, row in df.iterrows():
        instruction_ = instruction.format(prompt=row['Prompt'])
        output_text = row['Story']
        item = {
            "instruction": instruction_,
            "input": "",
            "output": f"# Output \n 【Story Content】\n {output_text}"
        }
        data_list.append(item)
    return data_list

train_data = format_data(train_df)
val_data = format_data(val_df)
test_data = format_data(test_df)

result = train_data + val_data + test_data

output_dir = "../StoryGeneration/DataV2"
os.makedirs(output_dir, exist_ok=True)

def save_to_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

save_to_json(train_data, os.path.join(output_dir, "train.json"))
save_to_json(val_data, os.path.join(output_dir, "val.json"))
save_to_json(test_data, os.path.join(output_dir, "test.json"))

print("\nDataset split statistics:")
print(f"Total data: {len(result)} items")
print(f"Training set: {len(train_data)} items ({len(train_data)/len(result)*100:.1f}%)")
print(f"Validation set: {len(val_data)} items ({len(val_data)/len(result)*100:.1f}%)")
print(f"Test set: {len(test_data)} items ({len(test_data)/len(result)*100:.1f}%)")
print(f"Since grouped by Prompt, the actual ratio may deviate slightly from 8:1:1, which is normal.")

print("\nVerifying if Prompts are independent in each dataset...")
train_instructions = {item['instruction'] for item in train_data}
val_instructions = {item['instruction'] for item in val_data}
test_instructions = {item['instruction'] for item in test_data}

assert len(train_instructions.intersection(val_instructions)) == 0, "Error: Training set and validation set have overlapping Instructions!"
assert len(train_instructions.intersection(test_instructions)) == 0, "Error: Training set and test set have overlapping Instructions!"
assert len(val_instructions.intersection(test_instructions)) == 0, "Error: Validation set and test set have overlapping Instructions!"

print("Verification successful: All Instructions are completely independent in training, validation, and test sets, with no overlap.")

dataset_info = {
    "total_samples": len(result),
    "train_samples": len(train_data),
    "val_samples": len(val_data),
    "test_samples": len(test_data),
    "train_ratio": len(train_data) / len(result),
    "val_ratio": len(val_data) / len(result),
    "test_ratio": len(test_data) / len(result),
    "split_strategy": "Grouped by unique Prompt to prevent data leakage",
    "unique_prompts_total": len(unique_prompts),
    "unique_prompts_train": len(train_prompts),
    "unique_prompts_val": len(val_prompts),
    "unique_prompts_test": len(test_prompts),
    "random_state": 42
}

info_path = os.path.join(output_dir, "dataset_info.json")
with open(info_path, "w", encoding="utf-8") as f:
    json.dump(dataset_info, f, ensure_ascii=False, indent=2)
print(f"\nDataset information saved to: {info_path}")

