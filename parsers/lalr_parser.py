class LALRParser:
    def __init__(self, grammar, tokens):
        self.grammar = grammar
        self.tokens = tokens

    def parse(self):
        print("\nLALR Parsing")
        print("Merging states...")
        print("Accepted (demo)")