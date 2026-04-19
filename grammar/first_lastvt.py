class FirstLastVT:
    def __init__(self, grammar):
        # Supports dict OR Grammar object
        if isinstance(grammar, dict):
            self.grammar = grammar
            self.non_terminals = list(grammar.keys())
        else:
            self.grammar = grammar.productions
            self.non_terminals = grammar.non_terminals

        # Detect terminals
        self.terminals = set()
        for head in self.grammar:
            for prod in self.grammar[head]:
                for sym in prod:
                    if sym not in self.non_terminals:
                        self.terminals.add(sym)

        self.firstvt = {nt: set() for nt in self.non_terminals}
        self.lastvt = {nt: set() for nt in self.non_terminals}

    def compute(self):
        self.compute_firstvt()
        self.compute_lastvt()

    # ---------------- FIRSTVT ----------------
    def compute_firstvt(self):
        changed = True
        while changed:
            changed = False
            for head, prods in self.grammar.items():
                for prod in prods:
                    if not prod:
                        continue

                    # A → a α
                    if prod[0] in self.terminals:
                        if prod[0] not in self.firstvt[head]:
                            self.firstvt[head].add(prod[0])
                            changed = True

                    # A → B α
                    if prod[0] in self.non_terminals:
                        for sym in self.firstvt[prod[0]]:
                            if sym not in self.firstvt[head]:
                                self.firstvt[head].add(sym)
                                changed = True

                        # A → B a α
                        if len(prod) > 1 and prod[1] in self.terminals:
                            if prod[1] not in self.firstvt[head]:
                                self.firstvt[head].add(prod[1])
                                changed = True

    # ---------------- LASTVT ----------------
    def compute_lastvt(self):
        changed = True
        while changed:
            changed = False
            for head, prods in self.grammar.items():
                for prod in prods:
                    if not prod:
                        continue

                    # A → α a
                    if prod[-1] in self.terminals:
                        if prod[-1] not in self.lastvt[head]:
                            self.lastvt[head].add(prod[-1])
                            changed = True

                    # A → α B
                    if prod[-1] in self.non_terminals:
                        for sym in self.lastvt[prod[-1]]:
                            if sym not in self.lastvt[head]:
                                self.lastvt[head].add(sym)
                                changed = True

                        # A → α a B
                        if len(prod) > 1 and prod[-2] in self.terminals:
                            if prod[-2] not in self.lastvt[head]:
                                self.lastvt[head].add(prod[-2])
                                changed = True

    # ---------------- PRINT ----------------
    def print_sets(self):
        print("\nFIRSTVT:")
        for nt in self.non_terminals:
            print(f"{nt} : {{ {', '.join(sorted(self.firstvt[nt]))} }}")

        print("\nLASTVT:")
        for nt in self.non_terminals:
            print(f"{nt} : {{ {', '.join(sorted(self.lastvt[nt]))} }}")