import numpy as np

def detect_patterns(sequence):
    first_pattern_index = None
    second_pattern_index = None
    
    # Pattern 1: Find the first instance where values stay below 1, then rise above 1.
    # We will iterate through the sequence to find the index for the last element below 1
    # just before the value rises above 1 for the first time.
    below_one_streak = True  # Flag to track if we are in a "below 1" region
    for i in range(1, len(sequence)):
        if below_one_streak and sequence[i] > 1 and sequence[i-1] <= 1:
            # First time we have a rise from <= 1 to > 1
            first_pattern_index = i - 1
            break
        if sequence[i] > 1:
            below_one_streak = False  # Break the "below one" streak

    # Pattern 2: Find the last instance where values stay above 1, then fall below 1.
    # We will iterate backwards to find the first element below 1 after the last segment above 1.
    above_one_streak = True
    for i in range(len(sequence) - 2, -1, -1):  # Start from the second to last element
        if above_one_streak and sequence[i] < 1 and sequence[i+1] >= 1:
            # Last drop from >= 1 to < 1
            second_pattern_index = i
            break
        if sequence[i] < 1:
            above_one_streak = False  # Break the "above one" streak

    return first_pattern_index, second_pattern_index

# Example usage
sequence = np.array([0.5, 0.6, 0.8, 1.1, 1.5, 2.0, 1.9, 0.9, 0.7, 0.5])  # Sample sequence
first_pattern, second_pattern = detect_patterns(sequence)

print("First Pattern Index:", first_pattern)
print("Second Pattern Index:", second_pattern)
