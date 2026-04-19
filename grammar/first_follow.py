class FirstFollow:
    def __init__(self, grammar):
        self.grammar = grammar

        # Initialize FIRST & FOLLOW
        self.first = {nt: set() for nt in grammar.non_terminals}
        self.follow = {nt: set() for nt in grammar.non_terminals}

        self.compute_first()
        self.compute_follow()

    # ---------------- FIRST ---------------- #
    def compute_first(self):
        changed = True

        while changed:
            changed = False

            for head in self.grammar.productions:
                for rule in self.grammar.productions[head]:

                    before = len(self.first[head])
                    add_epsilon = True  # track ε propagation

                    for symbol in rule:

                        # Case 1: ε
                        if symbol == 'ε':
                            self.first[head].add('ε')
                            add_epsilon = False
                            break

                        # Case 2: Terminal
                        elif symbol in self.grammar.terminals:
                            self.first[head].add(symbol)
                            add_epsilon = False
                            break

                        # Case 3: Non-terminal
                        elif symbol in self.first:
                            self.first[head] |= (self.first[symbol] - {'ε'})

                            if 'ε' not in self.first[symbol]:
                                add_epsilon = False
                                break

                        # Unknown symbol
                        else:
                            add_epsilon = False
                            break

                    # If all symbols derive ε
                    if add_epsilon:
                        self.first[head].add('ε')

                    if len(self.first[head]) > before:
                        changed = True

    # ---------------- FOLLOW ---------------- #
    def compute_follow(self):
        start = self.grammar.start_symbol
        self.follow[start].add('$')

        changed = True

        while changed:
            changed = False

            for head in self.grammar.productions:
                for rule in self.grammar.productions[head]:
                    for i in range(len(rule)):
                        B = rule[i]

                        if B in self.grammar.non_terminals:

                            before = len(self.follow[B])

                            # Case 1: A → αBβ
                            if i + 1 < len(rule):
                                beta = rule[i + 1:]
                                first_beta = set()

                                for symbol in beta:
                                    if symbol == 'ε':
                                        first_beta.add('ε')
                                        break

                                    elif symbol in self.grammar.terminals:
                                        first_beta.add(symbol)
                                        break

                                    elif symbol in self.first:
                                        first_beta |= (self.first[symbol] - {'ε'})

                                        if 'ε' not in self.first[symbol]:
                                            break
                                    else:
                                        break
                                else:
                                    first_beta.add('ε')

                                # Add FIRST(β) - ε
                                self.follow[B] |= (first_beta - {'ε'})

                                # If ε in FIRST(β), add FOLLOW(A)
                                if 'ε' in first_beta:
                                    self.follow[B] |= self.follow[head]

                            # Case 2: A → αB
                            else:
                                self.follow[B] |= self.follow[head]

                            if len(self.follow[B]) > before:
                                changed = True