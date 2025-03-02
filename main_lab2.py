
from src.finite_automation import FiniteAutomaton

# Variant 14:
# Q = {q0, q1, q2}
# Σ = {a, b, c}
# q0 = 'q0'
# F = {q2}
# δ:
#   q0: a -> {q0}, b -> {q1}
#   q1: a -> {q1}, c -> {q1, q2}
#   q2: a -> {q0}

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
print("Lab2:")
print("NFA is deterministic:", nfa.is_deterministic())

dfa = nfa.nfa_to_dfa()
print("\nConverted DFA from Variant 14 NFA:")
print("States:", dfa.Q)
print("Start State:", dfa.q0)
print("Final States:", dfa.F)
print("Transitions:")
for state, transitions in dfa.delta.items():
    for symbol, target in transitions.items():
        print(f"({state}, {symbol}) -> {target}")

grammar_from_dfa = dfa.to_regular_grammar()
print("\nRegular Grammar converted from DFA:")
for nonterminal, prods in grammar_from_dfa.productions.items():
    print(f"{nonterminal} -> {' | '.join(prods)}")
print("\nGrammar Classification:", grammar_from_dfa.classify())
