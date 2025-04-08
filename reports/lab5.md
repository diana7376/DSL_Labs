
# Lab4: Chomsky Normal Form Conversion

### Course: Formal Languages & Finite Automata  
Author: Iachim Diana
---

## Overview

This laboratory work focuses on implementing the conversion of context-free grammars to Chomsky Normal Form (CNF). The primary objective was to develop a systematic approach for transforming grammar productions through a series of normalization steps, culminating in CNF. The solution includes detailed visualization of each transformation step.

---

## Objectives

1. **Understand and explain** Chomsky Normal Form and its requirements
2. **Implement a grammar converter** that:
   - Eliminates ε-productions
   - Eliminates renaming (unit productions)
   - Removes inaccessible symbols
   - Removes non-productive symbols
   - Converts to proper CNF
3. **Visualize the transformation process** showing each normalization step

---

## Grammar Variant

The implementation handles the following grammar from **Variant 14**:

```
VN = {S, A, B, C, D}
VT = {a, b}
P = {
    1. S → aB
    2. S → A
    3. A → bAa
    4. A → aS
    5. A → a
    6. B → AbB
    7. B → BS
    8. B → a
    9. B → ε
    10. C → BA
    11. D → a
}
S is the start symbol
```

Key grammar features:
- ε-production (B → ε)
- Unit productions (S → A, B → A)
- Mixed-length productions
- Inaccessible symbols
- Non-productive symbols

---

## Implementation Description

The solution implements a systematic approach to CNF conversion through five distinct phases:

### Core Components

1. **Grammar Class**
   ```python
   class Grammar:
       def __init__(self, VN, VT, P, S):
           self.VN = set(VN)  # Non-terminals
           self.VT = set(VT)  # Terminals
           self.P = P         # Productions
           self.S = S         # Start symbol
   ```

2. **Transformation Methods**
   - `eliminate_epsilon()`: Removes ε-productions
   - `eliminate_renaming()`: Eliminates unit productions
   - `eliminate_inaccessible()`: Removes unreachable symbols
   - `eliminate_non_productive()`: Removes symbols that can't produce terminals
   - `to_cnf()`: Final conversion to CNF

3. **Step Tracking**
   ```python
   def print_step(step_name, grammar):
       print(f"\n=== {step_name} ===")
       print(grammar)
   ```

### Key Implementation Details

1. **Epsilon Elimination**
   - Identifies nullable symbols
   - Generates all possible combinations without nullable symbols

2. **Unit Production Elimination**
   - Uses a closure algorithm to replace chains like S→A→a with S→a

3. **CNF Conversion**
   - Breaks down long productions using new non-terminals
   - Ensures all productions are either:
     - A → BC (two non-terminals), or
     - A → a (single terminal)

### Example Transformation Flow

For production A → bAa:
1. Replace terminals with new non-terminals: X₁→b, X₂→a
2. Break into binary productions: A → X₁Y₁, Y₁→AY₂, Y₂→X₂

---

## Results and Examples

### Transformation Steps

**Original Grammar:**
```
S → aB | A
A → bAa | aS | a
B → AbB | BS | a | ε
C → BA
D → a
```

**After ε-elimination:**
```
S → aB | a | A
A → bAa | aS | a
B → AbB | Ab | bB | b | BS | B | a
C → BA
D → a
```

**After renaming elimination:**
```
S → aB | a | bAa | aS | a
A → bAa | aS | a
B → AbB | Ab | bB | b | BS | a
```

**After removing inaccessible symbols:**
```
S → aB | a | bAa | aS
A → bAa | aS | a
B → AbB | Ab | bB | b | BS | a
```

**Final CNF:**
```
X₁ → a
X₂ → b
S → X₁B | a | X₂Y₁ | X₁S
A → X₂Y₂ | X₁S | a
B → AY₃ | AY₄ | X₂B | b | BS | a
Y₁ → AX₁
Y₂ → AX₂
Y₃ → bB
Y₄ → b
```

---

## Challenges and Solutions

1. **ε-production Elimination**
   - Challenge: Determining all nullable symbols
   - Solution: Implemented fixed-point algorithm to find closure

2. **Unit Production Chains**
   - Challenge: Handling indirect chains like S→A→B→a
   - Solution: Used iterative replacement until no unit productions remain

3. **CNF Conversion**
   - Challenge: Breaking down productions like A→bAa
   - Solution: Introduced intermediate non-terminals systematically

4. **Symbol Tracking**
   - Challenge: Maintaining correct sets of symbols after each transformation
   - Solution: Implemented careful set operations and validation

---

## Conclusion

This lab work successfully demonstrates the step-by-step conversion of context-free grammars to Chomsky Normal Form, covering key transformations like eliminating ε-productions, unit productions, and non-productive symbols. It reinforced both practical skills and theoretical understanding of formal grammars. The clear visualization aided in verifying each stage, and the approach shows potential for broader use in compiler design and NLP tasks.

---

## References

1. [Chomsky Normal Form - Wikipedia](https://en.wikipedia.org/wiki/Chomsky_normal_form)
2. [Hopcroft, Motwani, Ullman - Introduction to Automata Theory](https://www.pearson.com/store/p/introduction-to-automata-theory-languages-and-computation/P100000582189)
3. [Python Documentation - Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
