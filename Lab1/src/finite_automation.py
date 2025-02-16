from Lab1.src.grammar import Grammar

class FiniteAutomaton:
    def __init__(self, grammar: Grammar, _delta: dict) -> None:
        self.Q = grammar.nonterminals + ['X']
        self.Alphabet = grammar.terminals
        self.q0 = grammar.start
        self.delta = _delta
        self.F = ['X']

    @classmethod
    def grammar_to_DFA(cls, grammar: Grammar) -> 'FiniteAutomaton':
        delta = {}
        for nonterminal, productions in grammar.productions.items():
            for production in productions:
                transition = production[0]
                result_state = production[1] if len(production) > 1 else 'X'
                delta.setdefault(nonterminal, {})[transition] = result_state
        return cls(grammar, delta)

    def word_belongs_to_language(self, string: str) -> bool:
        state = self.q0
        for char in string:
            if char not in self.Alphabet or state not in self.delta or char not in self.delta[state]:
                return False
            state = self.delta[state][char]
        return state in self.F
