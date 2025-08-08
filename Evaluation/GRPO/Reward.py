import re
import math

def compute_score(solution_str, ground_truth) -> float:
    """
    Calculate reward score
    
    Parameters:
    - solution_str: Solution string containing <ANSWER>score</ANSWER> tags
    - ground_truth: True score
    
    Returns:
    - float: Reward score (between 0-1)
    """
    if ground_truth is None:
        print(f"Warning: ground_truth is None, solution_str: {solution_str}")
        return 0.0  #
    # 1. Extract answer
    answer_pattern = r'<ANSWER>(\d+)</ANSWER>'
    match = re.search(answer_pattern, solution_str)
    
    if not match:
        # If no answer tag found, return 0
        return 0.0
    
    try:
        predicted_score = int(match.group(1))
    except ValueError:
        # If extracted value is not a valid number, return 0
        return 0.0
    
    # 2. Calculate score difference reward (weight 0.7)
    score_diff = abs(predicted_score - ground_truth)
    # Use exponential decay function, smaller difference means higher reward
    accuracy_reward = math.exp(-score_diff * 0.5)  # 0.5 is decay coefficient
    
    # 3. Calculate length reward (weight 0.3)
    solution_length = len(solution_str)
    # Set ideal length range (can be adjusted based on actual needs)
    min_ideal_length = 500   # Minimum ideal length
    max_ideal_length = 2000  # Maximum ideal length
    
    if solution_length < min_ideal_length:
        # Too short gets penalty
        length_reward = solution_length / min_ideal_length
    elif solution_length > max_ideal_length:
        # Too long also gets slight penalty (but won't drop to 0)
        length_reward = 0.8 + 0.2 * math.exp(-(solution_length - max_ideal_length) / 1000)
    else:
        # Give full score within ideal range
        length_reward = 1.0
    
    # 4. Combined reward
    # Accuracy weight 0.7, length weight 0.3
    total_reward = 0.7 * accuracy_reward + 0.3 * length_reward

    print(f"accuracy_reward: {accuracy_reward}, length_reward: {length_reward}")
    
    # 5. Extra reward: if completely correct, give full score
    if score_diff == 0:
        total_reward = min(1.0, total_reward + 0.1)  # Add 0.1 extra, but not exceed 1.0
    return round(total_reward, 4)

# Usage example
if __name__ == "__main__":
    # Test case 1: Completely correct answer
    solution1 = "After detailed analysis..." + "x" * 800 + "<ANSWER>4</ANSWER>"
    print(f"Case 1 score: {compute_score(solution1, 4)}")  # Should be close to 1.0
    
    # Test case 2: Answer off by 1 point
    solution2 = "After detailed analysis..." + "x" * 800 + "<ANSWER>3</ANSWER>"
    print(f"Case 2 score: {compute_score(solution2, 4)}")  # Should be between 0.5-0.7
    
    # Test case 3: Answer off by 2 points
    solution3 = "After detailed analysis..." + "x" * 800 + "<ANSWER>2</ANSWER>"
    print(f"Case 3 score: {compute_score(solution3, 4)}")  # Should be between 0.3-0.5
    
    # Test case 4: Too short answer
    solution4 = "Brief analysis<ANSWER>4</ANSWER>"
    print(f"Case 4 score: {compute_score(solution4, 4)}")  # Length penalty
    
    # Test case 5: Too long answer
    solution5 = "x" * 3000 + "<ANSWER>4</ANSWER>"
    print(f"Case 5 score: {compute_score(solution5, 4)}")  # Slight length penalty
