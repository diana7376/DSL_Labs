import random
import re
from typing import List, Tuple


def generate_from_regex(regex: str) -> str:
    """
    Generate a valid string from a regular expression pattern.
    Handles:
    - M? : M is optional
    - N{2} : exactly 2 N's
    - (O|P){3} : exactly 3 of either O or P
    - O* : 0 to 5 O's (limited)
    - R+ : 1 to 5 R's (limited)
    - (X|Y|Z){3} : exactly 3 of X, Y, or Z
    - 8+ : 1 to 5 8's (limited)
    - (9|O){2} : exactly 2 of 9 or O
    - (H|I) : exactly 1 of H or I
    - L* : 0 to 5 L's (limited)
    - N? : N is optional
    """
    result = []
    processing_steps = []

    # Process the regex pattern
    i = 0
    n = len(regex)

    while i < n:
        char = regex[i]
        processing_steps.append(f"Processing position {i}: '{char}'")

        if char == '?':  # Optional preceding character
            if random.choice([True, False]):
                result.append(result.pop())  # Keep the last character
            else:
                result.pop()  # Remove the last character
            i += 1

        elif char == '{':  # Quantifier
            # Find the closing brace
            j = regex.find('}', i)
            if j == -1:
                raise ValueError("Unclosed brace in regex")
            quantifier = regex[i + 1:j]

            if '|' in result[-1]:  # Handle alternation group
                group = result.pop()
                choices = group[1:-1].split('|')
                count = int(quantifier)
                selected = random.choices(choices, k=count)
                result.extend(selected)
            else:  # Simple repetition
                char_to_repeat = result.pop()
                count = int(quantifier)
                result.extend([char_to_repeat] * count)
            i = j + 1

        elif char == '(':  # Group start
            # Find the closing parenthesis
            j = regex.find(')', i)
            if j == -1:
                raise ValueError("Unclosed parenthesis in regex")
            group = regex[i:j + 1]
            result.append(group)
            i = j + 1

        elif char == '|':  # Part of alternation (handled in group processing)
            i += 1

        elif char == '*':  # 0 to 5 repetitions
            char_to_repeat = result.pop()
            count = random.randint(0, 5)
            result.extend([char_to_repeat] * count)
            i += 1

        elif char == '+':  # 1 to 5 repetitions
            char_to_repeat = result.pop()
            count = random.randint(1, 5)
            result.extend([char_to_repeat] * count)
            i += 1

        else:  # Literal character
            result.append(char)
            i += 1

    processing_steps.append("Final result construction")
    return ''.join(result), processing_steps


# Variant patterns
patterns = [
    "M?N{2}(O|P){3}O*R+",
    "(X|Y|Z){3}8+(9|O){2}",
    "(H|I)(J|K)L*N?"
]

# Generate examples for each pattern
for pattern in patterns:
    print(f"\nGenerating strings for pattern: {pattern}")
    for _ in range(3):  # Generate 3 examples per pattern
        result, steps = generate_from_regex(pattern)
        print(f"  Example: {result}")

    # Show processing steps for one generation
    print("\nProcessing steps example:")
    result, steps = generate_from_regex(pattern)
    for step in steps:
        print(f"  {step}")
    print(f"  Final result: {result}")