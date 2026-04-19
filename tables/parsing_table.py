class ParsingTable:
    def __init__(self):
        self.table = {}

    def add(self, nt, t, rule):
        self.table[(nt, t)] = rule

    def get(self, nt, t):
        return self.table.get((nt, t))