from src.grammar import Grammar

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

### lab2 ###
    @classmethod
    def from_definition(cls, Q: list, Alphabet: list, q0: str, delta: dict, F: list) -> 'FiniteAutomaton':
        """
        Create a FiniteAutomaton instance from a given definition.
        The delta parameter here can represent an NFA (with target sets).
        """
        instance = cls.__new__(cls)
        instance.Q = Q
        instance.Alphabet = Alphabet
        instance.q0 = q0
        instance.delta = delta
        instance.F = F
        return instance


    def is_deterministic(self) -> bool:
        """
        Returns True if the FA is deterministic (for every state and symbol,
        there is at most one target state), otherwise False.
        """
        for state in self.Q:
            if state in self.delta:
                for symbol, targets in self.delta[state].items():
                    # If targets is a set, check its size.
                    if isinstance(targets, set) and len(targets) > 1:
                        return False
        return True


    def _state_label(self, state_set: frozenset) -> str: #return a label (string) for a set of NFA states
        if not state_set:
            return '∅'
        return '_'.join(sorted(state_set))


    def nfa_to_dfa(self) -> 'FiniteAutomaton':
        """
        Converts an NFA (where delta maps to sets of states) into an equivalent DFA.
        Uses the subset (powerset) construction.
        """
        dfa_delta = {}  # will map state_label -> {symbol: state_label}
        state_mapping = {}  # maps frozenset of NFA states to state label
        new_states = []  # queue for processing

        start_set = frozenset([self.q0])
        start_label = self._state_label(start_set)
        state_mapping[start_set] = start_label
        dfa_states = [start_set]
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
                        # Ensure we add targets whether targets is a set or a single state.
                        if isinstance(targets, set):
                            target_set |= targets
                        else:
                            target_set.add(targets)
                target_set = frozenset(target_set)
                if target_set:
                    if target_set not in state_mapping:
                        state_mapping[target_set] = self._state_label(target_set)
                        dfa_states.append(target_set)
                        new_states.append(target_set)
                    dfa_delta[current_label][symbol] = state_mapping[target_set]
                else:
                    # Optionally add a sink state (here labeled as ∅)
                    sink = frozenset()
                    if sink not in state_mapping:
                        state_mapping[sink] = '∅'
                        dfa_states.append(sink)
                        # Sink state loops to itself on all symbols.
                        dfa_delta['∅'] = {s: '∅' for s in self.Alphabet}
                    dfa_delta[current_label][symbol] = '∅'

        # Build DFA Q, q0, and F:
        dfa_Q = list(state_mapping.values())
        dfa_q0 = state_mapping[start_set]
        dfa_F = []
        for state_set, label in state_mapping.items():
            if any(s in self.F for s in state_set):
                dfa_F.append(label)
        return FiniteAutomaton.from_definition(dfa_Q, self.Alphabet, dfa_q0, dfa_delta, dfa_F)


    def to_regular_grammar(self) -> Grammar:
        """
        Converts the FA (assumed to be deterministic) into a Regular Grammar.
        For each transition (p, a) -> q, we add the production: p -> a q.
        Additionally, for each final state, we add an epsilon production.
        """
        productions = {}
        # Add productions for each transition.
        for state in self.Q:
            if state in self.delta:
                for symbol, target in self.delta[state].items():
                    prod = symbol + target
                    productions.setdefault(state, []).append(prod)
        # For every final state, add an epsilon (empty string) production.
        for final_state in self.F:
            productions.setdefault(final_state, []).append("ε")
        return Grammar(self.Q, self.Alphabet, productions, self.q0)


