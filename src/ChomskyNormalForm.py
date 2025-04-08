class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = set(VN)  # Non-terminals
        self.VT = set(VT)  # Terminals
        self.P = P  # Productions (list of tuples)
        self.S = S  # Start symbol
        self.next_new_nonterminal = 1  # Counter for generating new non-terminals

    def __str__(self):
        productions = '\n'.join([f"{left} → {' '.join(right) if right != ('ε',) else 'ε'}"
                                 for left, right in sorted(self.P, key=lambda x: (x[0], x[1]))])
        return f"VN: {self.VN}\nVT: {self.VT}\nStart: {self.S}\nProductions:\n{productions}"

    def _get_new_nonterminal(self):
        """Generate a new unique non-terminal symbol"""
        new_nt = f"N{self.next_new_nonterminal}"
        self.next_new_nonterminal += 1
        return new_nt

    def eliminate_epsilon(self):
        # Step 1: Find all nullable non-terminals
        nullable = set()
        changed = True
        while changed:
            changed = False
            for left, right in self.P:
                if right == ('ε',) and left not in nullable:
                    nullable.add(left)
                    changed = True
                elif all(sym in nullable for sym in right) and left not in nullable:
                    nullable.add(left)
                    changed = True

        # Step 2: Generate new productions without nullable symbols
        new_productions = []
        for left, right in self.P:
            if right == ('ε',):
                continue  # Skip epsilon productions

            # Generate all possible combinations without nullable symbols
            positions = [i for i, sym in enumerate(right) if sym in nullable]
            n = len(positions)

            # Binary representation to generate all subsets
            for mask in range(1, 1 << n):
                new_right = list(right)
                bits = bin(mask)[2:].zfill(n)
                for i in range(n):
                    if bits[i] == '0':
                        new_right[positions[i]] = None  # Mark for removal
                new_right = [sym for sym in new_right if sym is not None]
                if new_right:  # Avoid empty productions
                    new_productions.append((left, tuple(new_right)))

            # Also add the original production if not all symbols are nullable
            if not all(sym in nullable for sym in right):
                new_productions.append((left, right))

        # Remove duplicates
        unique_productions = []
        seen = set()
        for prod in new_productions:
            if prod not in seen:
                seen.add(prod)
                unique_productions.append(prod)

        self.P = unique_productions
        return self

    def eliminate_renaming(self):
        # Step 1: Find all unit productions (A → B)
        changed = True
        while changed:
            changed = False
            new_productions = []
            unit_productions = []

            # Separate unit and non-unit productions
            for left, right in self.P:
                if len(right) == 1 and right[0] in self.VN:
                    unit_productions.append((left, right[0]))
                else:
                    new_productions.append((left, right))

            # For each unit production A → B, add all B's productions to A
            for A, B in unit_productions:
                for left, right in self.P:
                    if left == B and (A, right) not in new_productions:
                        new_productions.append((A, right))
                        changed = True

            self.P = new_productions

        return self

    def eliminate_inaccessible(self):
        # Find all reachable symbols from the start symbol
        reachable = {self.S}
        changed = True
        while changed:
            changed = False
            for left, right in self.P:
                if left in reachable:
                    for symbol in right:
                        if symbol in self.VN and symbol not in reachable:
                            reachable.add(symbol)
                            changed = True

        # Remove non-reachable non-terminals and their productions
        self.VN = {nt for nt in self.VN if nt in reachable}
        self.P = [(left, right) for left, right in self.P
                  if left in reachable and all(sym in self.VT or sym in reachable for sym in right)]

        return self

    def eliminate_non_productive(self):
        # Find all productive symbols (can derive terminal strings)
        productive = set()
        changed = True
        while changed:
            changed = False
            for left, right in self.P:
                if all(sym in self.VT or sym in productive for sym in right) and left not in productive:
                    productive.add(left)
                    changed = True

        # Remove non-productive non-terminals and their productions
        self.VN = {nt for nt in self.VN if nt in productive}
        self.P = [(left, right) for left, right in self.P
                  if left in productive and all(sym in self.VT or sym in productive for sym in right)]

        return self

    def to_cnf(self):
        # Step 1: Eliminate ε-productions
        self.eliminate_epsilon()

        # Step 2: Eliminate renaming (unit productions)
        self.eliminate_renaming()

        # Step 3: Eliminate inaccessible symbols
        self.eliminate_inaccessible()

        # Step 4: Eliminate non-productive symbols
        self.eliminate_non_productive()

        # Step 5: Convert to CNF
        new_productions = []
        terminal_replacements = {}  # Map terminals to new non-terminals

        # First handle terminal replacements
        for terminal in self.VT:
            new_nt = self._get_new_nonterminal()
            terminal_replacements[terminal] = new_nt
            self.VN.add(new_nt)
            new_productions.append((new_nt, (terminal,)))

        # Process all productions
        for left, right in self.P:
            if len(right) == 1 and right[0] in self.VT:
                # Already in correct form (A → a)
                new_productions.append((left, right))
            elif len(right) == 2 and all(sym in self.VN for sym in right):
                # Already in correct form (A → BC)
                new_productions.append((left, right))
            else:
                # Need to break down longer productions
                current_right = list(right)

                # Replace terminals with their corresponding non-terminals
                for i in range(len(current_right)):
                    if current_right[i] in self.VT:
                        current_right[i] = terminal_replacements[current_right[i]]

                # Break down into pairs
                while len(current_right) > 2:
                    new_nt = self._get_new_nonterminal()
                    self.VN.add(new_nt)
                    new_productions.append((new_nt, (current_right[0], current_right[1])))
                    current_right = [new_nt] + current_right[2:]

                # Add the final production
                new_productions.append((left, tuple(current_right)))

        self.P = new_productions
        return self


# def process_grammar(grammar):
#     """Process the grammar through all CNF steps and print results"""
#     steps = [
#         ("Original Grammar", lambda g: g),
#         ("Step 1: Eliminate ε-productions", lambda g: g.eliminate_epsilon()),
#         ("Step 2: Eliminate renaming", lambda g: g.eliminate_renaming()),
#         ("Step 3: Eliminate inaccessible symbols", lambda g: g.eliminate_inaccessible()),
#         ("Step 4: Eliminate non-productive symbols", lambda g: g.eliminate_non_productive()),
#         ("Step 5: Convert to Chomsky Normal Form", lambda g: g.to_cnf())
#     ]
#
#     for step_name, step_func in steps:
#         print(f"\n{step_name}:")
#         step_func(grammar)
#         print(grammar)
#
#
# # Your specific variant with epsilon production
# VN = {'S', 'A', 'B', 'C', 'D'}
# VT = {'a', 'b'}
# P = [
#     ('S', ('a', 'B')),
#     ('S', ('A',)),
#     ('A', ('b', 'A', 'a')),
#     ('A', ('a', 'S')),
#     ('A', ('a',)),
#     ('B', ('A', 'b', 'B')),
#     ('B', ('B', 'S')),
#     ('B', ('a',)),
#     ('B', ('ε',)),
#     ('C', ('B', 'A')),
#     ('D', ('a',))
# ]
# S = 'S'
#
# # Create and process the grammar
# grammar = Grammar(VN, VT, P, S)
# process_grammar(grammar)