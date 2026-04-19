class Preprocess:

    # ---------------- LEFT RECURSION ---------------- #
    def remove_left_recursion(self, grammar):
        new_productions = {}

        for A in grammar.productions:
            alpha = []  # left-recursive parts
            beta = []   # non-left-recursive parts

            for rule in grammar.productions[A]:
                if rule[0] == A:
                    alpha.append(rule[1:])
                else:
                    beta.append(rule)

            # If left recursion exists
            if alpha:
                A_dash = A + "'"

                new_productions[A] = []
                new_productions[A_dash] = []

                # A → β A'
                for b in beta:
                    new_productions[A].append(b + [A_dash])

                # A' → α A' | ε
                for a in alpha:
                    new_productions[A_dash].append(a + [A_dash])

                new_productions[A_dash].append(['ε'])

            else:
                new_productions[A] = grammar.productions[A]

        # Update grammar
        grammar.productions = new_productions
        grammar.non_terminals = set(new_productions.keys())

        return grammar


    # ---------------- LEFT FACTORING ---------------- #
    def left_factoring(self, grammar):
        new_productions = {}

        for A in grammar.productions:
            rules = grammar.productions[A]

            prefix_map = {}

            # Group rules by first symbol
            for rule in rules:
                prefix = rule[0]
                if prefix not in prefix_map:
                    prefix_map[prefix] = []
                prefix_map[prefix].append(rule)

            # Check if factoring needed
            if any(len(v) > 1 for v in prefix_map.values()):
                A_dash = A + "'"
                new_productions[A] = []
                new_productions[A_dash] = []

                for prefix in prefix_map:
                    group = prefix_map[prefix]

                    if len(group) > 1:
                        # A → prefix A'
                        new_productions[A].append([prefix, A_dash])

                        # A' → remaining parts
                        for rule in group:
                            if len(rule) > 1:
                                new_productions[A_dash].append(rule[1:])
                            else:
                                new_productions[A_dash].append(['ε'])
                    else:
                        new_productions[A].append(group[0])

            else:
                new_productions[A] = rules

        # Update grammar
        grammar.productions = new_productions
        grammar.non_terminals = set(new_productions.keys())

        return grammar