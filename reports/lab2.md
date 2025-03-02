# Lab 2: Determinism in Finite Automata, NDFA-to-DFA Conversion, and Chomsky Hierarchy

### Course: Formal Languages & Finite Automata
### Author: Diana Iachim

----

## Theory
&nbsp;&nbsp;&nbsp;&nbsp;Finite Automata are abstract machines used to model computation and recognize formal languages. A key property of these automata is determinism: in a Deterministic Finite Automaton (DFA), every state has exactly one transition per input symbol, whereas in a Non-deterministic Finite Automaton (NFA), a state may have multiple transitions for the same symbol. The subset (powerset) construction algorithm converts an NFA to an equivalent DFA. Moreover, regular grammars (Type-3 in the Chomsky hierarchy) can be derived from DFAs, linking grammar theory with automata.

## Objectives

* Implement a function in the Grammar class to classify grammars based on the Chomsky hierarchy.
* Convert a finite automaton into a regular grammar.
* Determine whether a finite automaton is deterministic or non-deterministic.
* Implement functionality to convert an NDFA to a DFA using the subset construction.

## Implementation Description

### **1. Grammar Class**
&nbsp;&nbsp;&nbsp;&nbsp;The `Grammar` class defines a formal grammar with non-terminals, terminals, production rules, and a start symbol. It includes methods for generating strings and classifying the grammar. The `classify()` method inspects each production to ensure it is either a single terminal, a terminal followed by a nonterminal, or the empty string ("ε"). If all productions conform to this format, the grammar is classified as "Regular (Type-3)".

#### **Key Method: `classify()`**
```python
def classify(self) -> str:
    """
    Classify the grammar based on the Chomsky hierarchy.
    Returns "Regular (Type-3)" if every production is either:
      - A single terminal symbol,
      - A terminal symbol followed by a nonterminal, or
      - The empty string (represented as "ε")
    Otherwise, returns "Not Regular".
    """
    for nonterminal, productions in self.productions.items():
        for prod in productions:
            if prod == "ε":
                continue
            if len(prod) == 1:
                if prod not in self.terminals:
                    return "Not Regular"
            elif len(prod) == 2:
                if prod[0] not in self.terminals or prod[1] not in self.nonterminals:
                    return "Not Regular"
            else:
                return "Not Regular"
    return "Regular (Type-3)"
```

### **2. Finite Automaton**
&ensp;&ensp;&ensp;The `FiniteAutomaton` class converts a grammar into an automaton, tests if strings belong to the language, and provides methods for advanced automata operations. For Lab 2, new functionalities include:

- Determinism Check: `is_deterministic()` iterates through each state's transitions to ensure there’s at most one target state per input.
- NFA-to-DFA Conversion: `nfa_to_dfa()` applies the subset construction algorithm to generate a DFA from an NFA.
- Conversion to Regular Grammar: `to_regular_grammar()` translates a DFA back into a regular grammar.
- Graphical Representation (Bonus): `to_dot()` generates a DOT description of the automaton, and visualize() uses Graphviz to render the diagram.

#### **Key Method: `is_deterministic()`**
```python
def is_deterministic(self) -> bool:
    """
    Returns True if the FA is deterministic (for every state and symbol,
    there is at most one target state), otherwise False.
    """
    for state in self.Q:
        if state in self.delta:
            for symbol, targets in self.delta[state].items():
                if isinstance(targets, set) and len(targets) > 1:
                    return False
    return True
```
#### **Key Method: `nfa_to_dfa()`**
```python
def nfa_to_dfa(self) -> 'FiniteAutomaton':
    """
    Converts an NFA (where delta maps to sets of states) into an equivalent DFA.
    Uses the subset (powerset) construction.
    """
    dfa_delta = {}
    state_mapping = {}
    new_states = []
    start_set = frozenset([self.q0])
    start_label = self._state_label(start_set)
    state_mapping[start_set] = start_label
    new_states.append(start_set)
    
    while new_states:
        current = new_states.pop(0)
        current_label = state_mapping[current]
        dfa_delta[current_label] = {}
        for symbol in self.Alphabet:
            target_set = set()
            for nfa_state in current:
                if nfa_state in self.delta and symbol in self.delta[nfa_state]:
                    targets = self.delta[nfa_state][symbol]
                    if isinstance(targets, set):
                        target_set |= targets
                    else:
                        target_set.add(targets)
            target_set = frozenset(target_set)
            if target_set:
                if target_set not in state_mapping:
                    state_mapping[target_set] = self._state_label(target_set)
                    new_states.append(target_set)
                dfa_delta[current_label][symbol] = state_mapping[target_set]
            else:
                sink = frozenset()
                if sink not in state_mapping:
                    state_mapping[sink] = '∅'
                    dfa_delta['∅'] = {s: '∅' for s in self.Alphabet}
                dfa_delta[current_label][symbol] = '∅'
    
    dfa_Q = list(state_mapping.values())
    dfa_q0 = state_mapping[start_set]
    dfa_F = []
    for state_set, label in state_mapping.items():
        if any(s in self.F for s in state_set):
            dfa_F.append(label)
    return FiniteAutomaton.from_definition(dfa_Q, self.Alphabet, dfa_q0, dfa_delta, dfa_F)
```
### **3. Main Script**
&ensp;&ensp;&ensp;The `main_lab2.py` file demonstrates the implementation:

- Variant 14 of the automaton is defined (with states `q0`, `q1`, `q2`; alphabet `{a, b, c}`; start state `q0`; final state `q2`; and specified transitions).
- The script checks if the NFA is deterministic, converts it into a DFA using the subset construction, and finally converts the DFA into a regular grammar.
- The results are printed, and (optionally) the DFA can be visualized using Graphviz.

#### **Code Snippet from Main Script:**
```python
variant14_Q = ['q0', 'q1', 'q2']
variant14_Alphabet = ['a', 'b', 'c']
variant14_q0 = 'q0'
variant14_F = ['q2']
variant14_delta = {
    'q0': {'a': {'q0'}, 'b': {'q1'}},
    'q1': {'a': {'q1'}, 'c': {'q1', 'q2'}},
    'q2': {'a': {'q0'}}
}

nfa = FiniteAutomaton.from_definition(variant14_Q, variant14_Alphabet, variant14_q0, variant14_delta, variant14_F)
print("NFA is deterministic:", nfa.is_deterministic())

dfa = nfa.nfa_to_dfa()
print("\nConverted DFA from Variant 14 NFA:")
print("States:", dfa.Q)
print("Start State:", dfa.q0)
print("Final States:", dfa.F)
for state, transitions in dfa.delta.items():
    for symbol, target in transitions.items():
        print(f"({state}, {symbol}) -> {target}")

grammar_from_dfa = dfa.to_regular_grammar()
print("\nRegular Grammar converted from DFA:")
for nonterminal, prods in grammar_from_dfa.productions.items():
    print(f"{nonterminal} -> {' | '.join(prods)}")
print("\nGrammar Classification:", grammar_from_dfa.classify())
```
## Conclusion

&ensp;&ensp;&ensp;In conclusion, this lab successfully extends the work from Lab 1 by incorporating advanced automata techniques. The implementation of the grammar classification method effectively determines whether a grammar is regular, while the subset construction algorithm reliably converts an NFA into an equivalent DFA. Furthermore, the conversion of the DFA back into a regular grammar illustrates the strong connection between automata and formal grammars. Additionally, the optional graphical representation feature using Graphviz offers a visual insight into the automaton's structure, thereby enhancing our understanding of the system's behavior. Overall, these implementations confirm that the system accurately addresses both the theoretical and practical aspects of formal language processing and automata conversion.

## References
1. [Video: Conversion of NFA to DFA](https://www.youtube.com/watch?v=jMxuL4Xzi_A)
2. [Video: Conversion from Finite automata into Regular Grammar](https://www.youtube.com/watch?v=ROeBNqwSLyg)
3. [University Course on Formal Languages](https://else.fcim.utm.md/course/view.php?id=98)
4. Other YouTube tutorials and online resources.