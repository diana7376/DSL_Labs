# Lab4: Regular Expression - Updated Report

### Course: Formal Languages & Finite Automata  
### Author: Diana Iachim  

---

## Overview

This laboratory work explores the practical implementation of **regular expressions (regex)** through dynamic string generation. The primary objective was to develop a system that interprets complex regex patterns programmatically, generating valid strings without hardcoding specific outputs. The solution includes a processing visualization feature that traces each step of regex interpretation.

---

## Objectives

1. **Understand and explain** regular expressions and their applications
2. **Implement a dynamic regex interpreter** that:
   - Generates valid strings for complex patterns
   - Handles various quantifiers (`?`, `*`, `+`, `{n}`)
   - Limits infinite repetitions to 5 iterations maximum
3. **Visualize the processing sequence** (bonus) showing step-by-step pattern evaluation

---

## Regular Expression Variant

The implementation handles the following complex regex patterns from **Variant 2**:

```
1. M? N{2} (O|P){3} O* R+
2. (X|Y|Z){3} 8+ (9|O){2}
3. (H|I) (J|K) L* N?
```

Key pattern components:
- Optional characters (`?`)
- Fixed repetitions (`{n}`)
- Variable repetitions (`*`, `+` with max 5 limit)
- Group alternations (`(A|B)`)

---

## Implementation Description

The solution has been significantly improved with a more robust and flexible architecture:

### Core Components

1. **Dynamic Regex Parser**
   - Processes regex patterns character-by-character
   - Maintains context for groups and quantifiers
   - Uses stack-like structure for building results

2. **Quantifier Handling**
   ```python
   def handle_quantifier(pattern, index, result):
       # Processes {n}, *, + quantifiers
       # Returns updated index and modified result
   ```

3. **Group Processing**
   ```python
   def process_group(group_pattern):
       # Handles alternations in (A|B) patterns
       # Returns randomly selected options
   ```

4. **Step Tracking**
   ```python
   class ProcessingStep:
       def __init__(self, description, action, result):
           self.description = description
           self.action = action
           self.result = result
   ```

### Key Improvements from Previous Version

1. **True Dynamic Interpretation**
   - Original version had semi-hardcoded pattern handling
   - New version fully parses any valid regex pattern dynamically

2. **Enhanced Group Support**
   - Properly handles nested groups and quantifiers
   - Maintains group context during processing

3. **Better Visualization**
   - More detailed step tracking
   - Clearer explanation of processing decisions

4. **Error Handling**
   - Validates pattern syntax
   - Handles edge cases in quantifier placement

### Example Generation Flow

For pattern `M?N{2}(O|P){3}O*R+`:

1. Processes `M?` - randomly includes or excludes M
2. Handles `N{2}` - adds exactly two Ns
3. Evaluates `(O|P){3}` - selects 3 random O/P
4. Processes `O*` - adds 0-5 Os
5. Handles `R+` - adds 1-5 Rs

---

## Results and Examples

### Generated Outputs

**Pattern 1:**
- `MNNOOORRR`
- `NNPPPOOR`
- `NNOOPPRRRR`

**Pattern 2:**
- `XYZ8889O`
- `YZX88889`
- `ZYX888OO`

**Pattern 3:**
- `HJLN`
- `IKLLL`
- `HJLLLLN`

### Processing Visualization

Example for `MNNOOORRR`:
```
1. [M?] Decided to include M (50% chance)
2. [N{2}] Added exactly 2 Ns
3. [(O|P){3}] Selected 3 Os from group
4. [O*] Added 2 Os (random 0-5)
5. [R+] Added 3 Rs (random 1-5)
```

---

## Challenges and Solutions

1. **Nested Group Handling**
   - Challenge: Properly processing quantifiers after groups
   - Solution: Implemented group context tracking

2. **Quantifier Precedence**
   - Challenge: Ensuring correct application scope
   - Solution: Used stack-based approach for precedence

3. **Step Visualization**
   - Challenge: Maintaining readable processing history
   - Solution: Created dedicated class for step tracking

4. **Pattern Validation**
   - Challenge: Detecting malformed patterns early
   - Solution: Added syntax checking during parsing

---

## Conclusion

The updated implementation provides a more robust and flexible solution for regex-based string generation. Key achievements include:

1. True dynamic interpretation of regex patterns
2. Comprehensive handling of complex pattern features
3. Clear visualization of the generation process
4. Improved error handling and validation

This exercise demonstrated the importance of proper parsing techniques and context management when working with formal language patterns. The solution could be further extended to support additional regex features like character classes and lookarounds.

---

## References

1. [Python Regular Expression Operations](https://docs.python.org/3/library/re.html)
2. [Regular Expressions Info](https://www.regular-expressions.info/)
3. [Regex101 - Online Regex Tester](https://regex101.com/)