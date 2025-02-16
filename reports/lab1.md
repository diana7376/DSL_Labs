# Finite Automata and Regular Grammars

### Course: Formal Languages and Finite Automata
### Author: Diana Iachim  

----

## Theory
Finite Automata (FA) and Regular Grammars (RG) are fundamental concepts in Formal Languages and Automata Theory. A **grammar** is a set of rules that generates strings, while an **automaton** is a model that recognizes or accepts strings based on state transitions. Regular grammars can be converted into finite automata, which can determine whether a given input string belongs to a language.

In this implementation, a **Grammar class** is used to define a set of production rules and generate words. The **FiniteAutomaton class** converts a grammar into a deterministic finite automaton (DFA) and validates strings against the defined language.

## Objectives

* Implement a class for defining a regular grammar.
* Create a function to generate 5 valid strings from the grammar.
* Implement a method to convert a grammar into a finite automaton.
* Provide functionality in the finite automaton to check if a string belongs to the language.

## Implementation Description

### **1. Grammar Class**
The `Grammar` class represents a formal language with non-terminals, terminals, production rules, and a starting symbol. It provides methods for generating valid words.

#### **Key Methods:**
- `generate_string()`: Recursively replaces non-terminals with productions until a terminal string is formed.
- `generate_words()`: Calls `generate_string()` multiple times to create a list of 5 unique words.

#### **Code snippet:**
```python
class Grammar:
    def generate_words(self, num_strings=5) -> list:
        words = set()
        while len(words) < num_strings:
            words.add(self.generate_string())
        return list(words)
```

### **2. Finite Automaton Class**
The `FiniteAutomaton` class converts a given grammar into a deterministic finite automaton (DFA). It maintains states, transitions, and alphabet rules for recognizing words.

#### **Key Methods:**
- `grammar_to_DFA()`: Converts grammar rules into a transition table.
- `word_belongs_to_language()`: Simulates the DFA's state transitions to determine if a given string is accepted.

#### **Code snippet:**
```python
class FiniteAutomaton:
    def word_belongs_to_language(self, string: str) -> bool:
        state = self.q0
        for char in string:
            if char not in self.Alphabet or state not in self.delta or char not in self.delta[state]:
                return False
            state = self.delta[state][char]
        return state in self.F
```

### **3. Main Script**
The `main.py` script demonstrates the functionality by:
- Creating a `Grammar` instance with predefined rules.
- Generating and printing valid words from the grammar.
- Converting the grammar into a DFA.
- Checking if a given word belongs to the language.

#### **Code snippet:**
```python
# Generate and display valid words
print("Generated Strings:")
generated_strings = grammar_instance.generate_words()
for i, word in enumerate(generated_strings, 1):
    print(f"{i}: {word}")
```

## Conclusions / Results

The implementation successfully demonstrates:
- The generation of valid words based on regular grammar rules.
- The conversion of grammar into a finite automaton.
- The ability to check whether a string is accepted by the automaton.

The project meets all the objectives and can be expanded with additional features, such as visualization of the finite automaton’s state transitions.

## References
1. [Video: Introduction to Finite Automata](https://www.youtube.com/watch?v=9syvZr-9xwk)
2. [University Course on Formal Languages](https://else.fcim.utm.md/course/view.php?id=98)
3. Other YouTube tutorials and online resources.


