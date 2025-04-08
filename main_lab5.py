from src.ChomskyNormalForm import Grammar


def create_grammar():
    """Create and return the grammar from variant 14"""
    VN = {'S', 'A', 'B', 'C', 'D'}
    VT = {'a', 'b'}
    P = [
        ('S', ('a', 'B')),
        ('S', ('A',)),
        ('A', ('b', 'A', 'a')),
        ('A', ('a', 'S')),
        ('A', ('a',)),
        ('B', ('A', 'b', 'B')),
        ('B', ('B', 'S')),
        ('B', ('a',)),
        ('B', ('ε',)),
        ('C', ('B', 'A')),
        ('D', ('a',))
    ]
    S = 'S'
    return Grammar(VN, VT, P, S)


def process_grammar_steps(grammar):
    """Process the grammar through all CNF steps and print results"""
    steps = [
        ("Original Grammar", lambda g: g),
        ("After ε-elimination", lambda g: g.eliminate_epsilon()),
        ("After renaming elimination", lambda g: g.eliminate_renaming()),
        ("After removing inaccessible", lambda g: g.eliminate_inaccessible()),
        ("After removing non-productive", lambda g: g.eliminate_non_productive()),
        ("Chomsky Normal Form", lambda g: g.to_cnf())
    ]

    for step_name, step_func in steps:
        print(f"\n=== {step_name} ===")
        step_func(grammar)
        print(grammar)


def main():
    """Main function to run the grammar normalization"""
    print("=== Grammar Normalization to CNF ===")
    grammar = create_grammar()
    process_grammar_steps(grammar)


if __name__ == "__main__":
    main()