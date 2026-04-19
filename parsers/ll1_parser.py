class LL1Parser:
    def __init__(self, grammar, ff, tokens):
        self.grammar = grammar
        self.first = ff.first
        self.follow = ff.follow

        # Avoid double $
        if tokens and tokens[-1] == '$':
            self.tokens = tokens
        else:
            self.tokens = tokens + ['$']

        self.table = {}

    # -------------------------------
    # PRINT FIRST
    # -------------------------------
    def print_first(self):
        print("\nFIRST SET:")
        for nt in self.first:
            print(f"FIRST({nt}) = {self.first[nt]}")

    # -------------------------------
    # PRINT FOLLOW
    # -------------------------------
    def print_follow(self):
        print("\nFOLLOW SET:")
        for nt in self.follow:
            print(f"FOLLOW({nt}) = {self.follow[nt]}")

    # -------------------------------
    # BUILD TABLE
    # -------------------------------
    def build_table(self):
        for head in self.grammar.productions:
            for rule in self.grammar.productions[head]:

                first_alpha = set()

                for symbol in rule:
                    if symbol == 'ε':
                        first_alpha.add('ε')
                        break

                    elif symbol in self.grammar.terminals:
                        first_alpha.add(symbol)
                        break

                    elif symbol in self.first:
                        first_alpha |= (self.first[symbol] - {'ε'})

                        if 'ε' not in self.first[symbol]:
                            break
                    else:
                        break
                else:
                    first_alpha.add('ε')

                for terminal in (first_alpha - {'ε'}):
                    self.table[(head, terminal)] = rule

                if 'ε' in first_alpha:
                    for terminal in self.follow[head]:
                        self.table[(head, terminal)] = rule

    # -------------------------------
    # PRINT TABLE (FIXED)
    # -------------------------------
    def print_table(self):
        print("\nPARSING TABLE:\n")

        # ✅ FIX: dynamic terminals
        terminals = list(self.grammar.terminals)

        if '$' not in terminals:
            terminals.append('$')

        terminals = sorted(terminals)

        non_terminals = list(self.grammar.productions.keys())

        col_width = 12

        def print_border():
            print("+" + "+".join(["-" * col_width for _ in range(len(terminals) + 1)]) + "+")

        print_border()
        print("|{:<{w}}".format("NT", w=col_width), end="")
        for t in terminals:
            print("|{:<{w}}".format(t, w=col_width), end="")
        print("|")
        print_border()

        for nt in non_terminals:
            print("|{:<{w}}".format(nt, w=col_width), end="")

            for t in terminals:
                if (nt, t) in self.table:
                    rule = self.table[(nt, t)]
                    rule_str = nt + "->" + "".join(rule)
                    print("|{:<{w}}".format(rule_str, w=col_width), end="")
                else:
                    print("|{:<{w}}".format("-", w=col_width), end="")

            print("|")
            print_border()

    # -------------------------------
    # PARSING PROCESS
    # -------------------------------
    def parse(self):
        self.print_first()
        self.print_follow()

        self.build_table()
        self.print_table()

        print("\nSTEPS:\n")

        col_width = 20

        print(f"{'Stack':<{col_width}}{'Input':<{col_width}}{'Action':<{col_width}}")
        print("-" * (col_width * 3))

        stack = ['$']
        start = self.grammar.start_symbol
        stack.append(start)

        i = 0

        while stack:
            top = stack[-1]
            current = self.tokens[i]

            stack_str = "".join(stack[::-1])
            input_str = "".join(self.tokens[i:])

            # MATCH
            if top == current:
                action = f"match {current}"
                print(f"{stack_str:<{col_width}}{input_str:<{col_width}}{action:<{col_width}}")

                stack.pop()
                i += 1

            # NON-TERMINAL
            elif (top, current) in self.table:
                rule = self.table[(top, current)]
                action = f"{top} → {''.join(rule)}"

                print(f"{stack_str:<{col_width}}{input_str:<{col_width}}{action:<{col_width}}")

                stack.pop()

                if rule != ['ε']:
                    for sym in reversed(rule):
                        stack.append(sym)

            else:
                print(f"{stack_str:<{col_width}}{input_str:<{col_width}}❌ ERROR")
                return

        if i == len(self.tokens):
            print("\n✔ ACCEPTED")
        else:
            print("\n❌ REJECTED")