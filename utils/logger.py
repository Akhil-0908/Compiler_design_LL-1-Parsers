class Logger:
    def __init__(self):
        self.steps = []

    def log(self, stack, input_, action):
        self.steps.append((stack.copy(), input_.copy(), action))

    def show(self):
        print("\nSTACK\tINPUT\tACTION")
        for s in self.steps:
            print(s[0], "\t", s[1], "\t", s[2])