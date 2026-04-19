class CLRParser:
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens

    def parse(self):
        print("\nCLR Parsing")
        print("Building LR(1)...")
        print("Accepted (demo)")