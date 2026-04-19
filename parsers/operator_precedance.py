from grammar.first_lastvt import FirstLastVT


class OperatorPrecedenceParser:
    def __init__(self, grammar, start_symbol, tokens):
        self.grammar = grammar
        self.start_symbol = start_symbol
        # Avoid duplicate $
        if tokens and tokens[-1] == '$':
           self.tokens = tokens
        else:
           self.tokens = tokens + ['$']

        self.non_terminals = list(grammar.keys())

        # Detect terminals
        self.terminals = set()
        for head in grammar:
            for prod in grammar[head]:
                for sym in prod:
                    if sym not in self.non_terminals:
                        self.terminals.add(sym)

        self.terminals.add('$')

        # FIRSTVT & LASTVT
        fl = FirstLastVT(grammar)
        fl.compute()

        self.firstvt = fl.firstvt
        self.lastvt = fl.lastvt

        fl.print_sets()

        # Precedence table
        self.table = {a: {b: '' for b in self.terminals} for a in self.terminals}
        self.build_table()

    # ---------------- SET RELATION ----------------
    def set_relation(self, a, b, val):
        if self.table[a][b] != '' and self.table[a][b] != val:
            print(f"⚠ Conflict at ({a}, {b}) : {self.table[a][b]} vs {val}")
        self.table[a][b] = val

    # ---------------- CHECK OPERATOR GRAMMAR ----------------
    def is_operator_grammar(self):
        for head in self.grammar:
            for prod in self.grammar[head]:

                # No epsilon
                if len(prod) == 0:
                    return False

                # No adjacent non-terminals
                for i in range(len(prod) - 1):
                    if (prod[i] in self.non_terminals and
                            prod[i + 1] in self.non_terminals):
                        return False

        return True

    # ---------------- BUILD TABLE ----------------
    def build_table(self):
        for head in self.grammar:
            for prod in self.grammar[head]:

                for i in range(len(prod) - 1):

                    # a = b
                    if prod[i] in self.terminals and prod[i + 1] in self.terminals:
                        self.set_relation(prod[i], prod[i + 1], '=')

                    # a < FIRSTVT(B)
                    if prod[i] in self.terminals and prod[i + 1] in self.non_terminals:
                        for b in self.firstvt[prod[i + 1]]:
                            self.set_relation(prod[i], b, '<')

                    # LASTVT(B) > a
                    if prod[i] in self.non_terminals and prod[i + 1] in self.terminals:
                        for a in self.lastvt[prod[i]]:
                            self.set_relation(a, prod[i + 1], '>')

                # a B b → a = b
                for i in range(len(prod) - 2):
                    if (prod[i] in self.terminals and
                        prod[i + 1] in self.non_terminals and
                        prod[i + 2] in self.terminals):
                        self.set_relation(prod[i], prod[i + 2], '=')

        # $ relations
        for a in self.firstvt[self.start_symbol]:
            self.set_relation('$', a, '<')

        for a in self.lastvt[self.start_symbol]:
            self.set_relation(a, '$', '>')

        self.table['$']['$'] = '='

    # ---------------- PRINT TABLE ----------------
    def print_table(self):
        print("\nOperator Precedence Table:")

        # Fixed order for clarity
        symbols = ['+', '*', '(', ')', 'id', '$']

        print("    ", end="")
        for s in symbols:
            print(f"{s:4}", end="")
        print()

        for row in symbols:
            print(f"{row:4}", end="")
            for col in symbols:
                print(f"{self.table[row][col]:4}", end="")
            print()

    # ---------------- PARSE ----------------
    def parse(self):
        self.print_table()

        stack = ['$']
        input_buffer = self.tokens.copy()

        print("\nParsing Steps:")
        print(f"{'Stack':<20}{'Input':<20}{'Action'}")

        while True:

            # Find top terminal in stack
            i = len(stack) - 1
            while stack[i] not in self.terminals:
                i -= 1

            top = stack[i]

            if not input_buffer:
                print("ERROR: Input empty")
                return False

            current = input_buffer[0]

            # ✅ ACCEPT CONDITION (FIXED)
            if top == '$' and current == '$':
                print(f"{''.join(stack):<20}{''.join(input_buffer):<20}ACCEPTED")
                return True

            relation = self.table[top].get(current, '')

            print(f"{''.join(stack):<20}{''.join(input_buffer):<20}", end="")

            # SHIFT
            if relation in ['<', '=']:
                print("SHIFT")
                stack.append(input_buffer.pop(0))

            # REDUCE
            elif relation == '>':
                print("REDUCE")
                while True:
                    last = stack.pop()
                    if stack[-1] in self.terminals:
                        if self.table[stack[-1]][last] == '<':
                            break

            else:
                print("ERROR")
                return False