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
