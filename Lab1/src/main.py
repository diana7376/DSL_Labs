
from Lab1.src.grammar import Grammar
from Lab1.src.finite_automation import FiniteAutomaton


grammar_rules = {
    'S': ['aS', 'bB'],
    'B': ['cB', 'd', 'aD'],
    'D': ['aB', 'b']
}

grammar_instance = Grammar(['S', 'B', 'D'], ['a', 'b', 'c', 'd'], grammar_rules, 'S')

# 5 valid strings from the grammar
print("Generated Strings:")
generated_strings = grammar_instance.generate_words()
for i, word in enumerate(generated_strings, 1):
    print(f"{i}: {word}")

# convert Grammar to Finite Automaton
finite_automaton_instance = FiniteAutomaton.grammar_to_DFA(grammar_instance)

# Display Finite Automaton details
print("\nFinite Automaton Details:")
print("States:", finite_automaton_instance.Q)
print("Alphabet:", finite_automaton_instance.Alphabet)
print("Start State:", finite_automaton_instance.q0)
print("Transitions:")
for state, transitions in finite_automaton_instance.delta.items():
    for symbol, result_state in transitions.items():
        print(f"({state}, {symbol}) -> {result_state}")

# check if a string belongs to the language
input_string = "aabcd"
result = finite_automaton_instance.word_belongs_to_language(input_string)
print(f"\nThe string '{input_string}' belongs to the language: {result}")
