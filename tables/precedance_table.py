class PrecedenceTable:
    def __init__(self):
        self.precedence = {'+': 1, '*': 2}

    def lower(self, op1, op2):
        return self.precedence.get(op1, 0) < self.precedence.get(op2, 0)