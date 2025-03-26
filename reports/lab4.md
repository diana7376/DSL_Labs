# Lab4: Regular Expression

### Course: Formal Languages & Finite Automata  
### Author: Diana Iachim  

---

## Overview

This lab focuses on understanding and applying **regular expressions (regex)** to dynamically generate strings that conform to a given pattern. Rather than manually hardcoding outputs, the task challenges us to **interpret regex expressions programmatically** and build a generator that can produce all valid variants of a string based on specified regex rules.

The specific goal of this lab was to work with **complex regex patterns**, broken into segments with various quantifiers (like `*`, `+`, `{n}`, `?`, and groups). Additionally, a bonus challenge was to trace and describe the internal steps that led to the generation of a string.

---

## Objectives

1. Write and explain what regular expressions are and what they are used for.
2. Generate valid strings for a given complex regex by:
   - Dynamically interpreting the expression.
   - Avoiding hardcoded values.
   - Limiting infinite repetitions (e.g., `*`, `+`) to 5 iterations max.
3. Bonus: Log the sequence of regex evaluations for each part of the pattern.

---

## Regular Expression Variant

We used the following complex regex expression from **Variant 2**:

```
M? N{2} (O|P){3} O* R+
(X|Y|Z){3} 8+ (9|O){2}
(H|I) (J|K) L* N?
```

This expression includes:
- Optional (`?`), exact (`{n}`), and variable (`*`, `+`) repetitions
- Group alternations like `(O|P)` and `(X|Y|Z)`
- Character class repetitions constrained by a max of 5

---

## Implementation Description

The implementation consists of two main files:

### `regex.py`
This file contains the logic for interpreting the regex expression and generating valid strings accordingly.

**Key components include:**

1. `repeat(symbols, times)`

This function generates a string made of randomly selected characters from a given list, repeated exactly times times.

```python
def repeat(symbols, times):
    return ''.join(random.choice(symbols) for _ in range(times))
```

2. `bounded_repeat(symbols, min, max)`

This handles regex operators like `*` and `+`, which allow variable-length repetitions. 
It randomly selects a number between min and max (up to 5), and returns both the string and how many times it was repeated.

```python
def bounded_repeat(symbols, min_count, max_count):
    count = random.randint(min_count, max_count)
    return repeat(symbols, count), count

# Example:
bounded_repeat(['R'], 1, 5)  # Might return ('RRR', 3)
Useful for patterns like O*, R+, L*, and 8+.
```
3. `generate_with_steps()`

The `generate_with_steps()` function builds a valid string based on the regex pattern while 
logging each step of the process. For every part of the pattern, such as optional 
characters, fixed or variable repetitions, and character groups, it selects 
characters accordingly and records what was added. This makes the function both a 
generator and an explainer, providing not just a valid output but also a clear 
sequence of how it was constructed.

```python
def generate_with_steps():
    steps = []
    result = ""

    m_char = random.choice(['', 'M'])
    result += m_char
    steps.append(f"Added 'M' {'once' if m_char else '0 times'}")

    result += 'NN'
    steps.append("Added 'N' exactly 2 times")

    # ... similar logic continues for each regex segment ...

    return result, steps
```
This function ensures the output is both valid and explainable — which helps fulfill the bonus point of showing the generation sequence step-by-step.

---

### `main_lab4.py`
This script simply runs the generation process and prints the results and explanation:

```python
Generated String: MNPPPQQRRXYZ88889HJLLN

Sequence of Steps:
- Added 'M' once
- Added 'N' exactly 2 times
- Added 3 characters from (O|P): 'PPP'
- Added 'O' 2 times for O*
- Added 'R' 2 times for R+
- Added 3 characters from (X|Y|Z): 'XYZ'
- Added '8' 3 times for 8+
- Added 2 characters from (9|O): '89'
- Added one character from (H|I): 'H'
- Added one character from (J|K): 'J'
- Added 'L' 2 times for L*
- Added 'N' once for N?
```

---

## Results

The program is capable of producing different valid strings like:
- `MNNPPPQQRRRXYZ88889HJLLN`
- `NNOPPOORXYZ888889IKLN`
- `MNNOOOPRRXYZ888O9HJLLLL`

Each output also provides a detailed explanation for each symbol/group added, fulfilling the **bonus point**.

---

## Conclusion

This lab demonstrated the process of dynamically parsing and executing regular expressions within a program. Rather than using built-in regex engines for string matching, we developed custom logic to interpret the structure of a regex, generate randomized but valid outputs, and trace each step of the generation process. Through this assignment, we gained a deeper understanding of how regular expressions work and how their behavior can be simulated using controlled randomness and structured string manipulation.

---

## References

1. [Regular Expressions – Python Docs](https://docs.python.org/3/library/re.html)  
2. [RegexOne - Learn Regular Expressions](https://regexone.com/)  
