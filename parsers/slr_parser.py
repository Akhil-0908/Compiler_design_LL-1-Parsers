class SLRParser:
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens

    def parse(self):
        print("\nSLR Parsing")
        print("Building LR(0)...")
        print("Accepted (demo)")