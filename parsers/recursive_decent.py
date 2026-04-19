class RecursiveDescentParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def match(self, t):
        if self.tokens[self.i] == t:
            print("Matched:", t)
            self.i += 1
        else:
            raise Exception("Error")

    def E(self):
        self.T()
        while self.tokens[self.i] == '+':
            self.match('+')
            self.T()

    def T(self):
        self.F()
        while self.tokens[self.i] == '*':
            self.match('*')
            self.F()

    def F(self):
        if self.tokens[self.i].isalpha():
            self.match(self.tokens[self.i])
        elif self.tokens[self.i] == '(':
            self.match('(')
            self.E()
            self.match(')')

    def parse(self):
        self.E()
        if self.tokens[self.i] == '$':
            print("Accepted")