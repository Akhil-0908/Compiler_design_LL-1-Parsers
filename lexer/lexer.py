import re

class Lexer:
    def tokenize(self, text):
        tokens = re.findall(r'[a-zA-Z]+|\+|\*|\(|\)', text)
        return tokens + ['$']