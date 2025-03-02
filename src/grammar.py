import random

class Grammar:
    def __init__(self, _VN: list, _VT: list, _P: dict, _S: str) -> None:
        self.nonterminals = _VN
        self.terminals = _VT
        self.productions = _P
        self.start = _S

    def generate_string(self, word=None) -> str:
        current_word = self.start if word is None else word
        while not self.terminal_word(current_word):
            for char in current_word:
                if char in self.productions:
                    production = random.choice(self.productions[char])
                    current_word = current_word.replace(char, production, 1)
                    break  # only replace the first non-terminal occurrence per step
        return current_word

    def terminal_word(self, word: str) -> bool:
        return all(char in self.terminals for char in word)

    def generate_words(self, num_strings=5) -> list:
        words = set()
        while len(words) < num_strings:
            words.add(self.generate_string())
        return list(words)

    ### lab2 ###
    def classify(self) -> str:
        """
        Classify the grammar based on the Chomsky hierarchy.
        Returns "Regular (Type-3)" if every production is either:
          - A single terminal symbol, or
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
                    # Check that the first character is a terminal and the second is a nonterminal.
                    if prod[0] not in self.terminals or prod[1] not in self.nonterminals:
                        return "Not Regular"
                else:
                    return "Not Regular"
        return "Regular (Type-3)"