import re

class Grammar:
    def __init__(self, productions):
        self.productions = {}
        self.non_terminals = set()
        self.terminals = set()
        self.start_symbol = None

        for prod in productions:
            if "->" not in prod:
                raise ValueError(f"Invalid production (missing '->'): {prod!r}")

            left, right = prod.split("->", 1)
            left = left.strip()

            if self.start_symbol is None:
                self.start_symbol = left

            self.non_terminals.add(left)

            # Allow either '|' or '/' as alternation separators
            right = right.replace("/", "|")
            rules = right.split("|")

            self.productions[left] = [
                self._tokenize_rhs(r.strip()) for r in rules
            ]

        self._find_terminals()

    # ---------------- TOKENIZER ---------------- #
    def _tokenize_rhs(self, rhs: str):
        if not rhs:
            return []

        # Supports:
        # E+T, (E), id, E + T, etc.
        token_re = re.compile(r"[A-Za-z_][A-Za-z0-9_']*|ε|\+|\*|\(|\)")
        tokens = token_re.findall(rhs.replace(" ", ""))

        if not tokens:
            raise ValueError(f"Invalid RHS in production: {rhs!r}")

        return tokens

    # ---------------- FIND TERMINALS ---------------- #
    def _find_terminals(self):
        for head in self.productions:
            for rule in self.productions[head]:
                for symbol in rule:
                    # Ignore epsilon
                    if symbol not in self.productions and symbol != 'ε':
                        self.terminals.add(symbol)

    # ---------------- PRINT GRAMMAR ---------------- #
    def print_grammar(self, title="Grammar"):
        print(f"\n{title}")
        for head in self.productions:
            rules = [" ".join(rule) for rule in self.productions[head]]
            print(f"{head} -> {' | '.join(rules)}")