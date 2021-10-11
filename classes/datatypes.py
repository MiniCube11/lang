class Number:
    def __init__(self, token):
        self.start = token.start
        self.value = token.value
        self.line = token.line
        self.program = token.program

    def __repr__(self):
        return f"(Number: {self.value})"


class String:
    def __init__(self, token):
        self.start = token.start
        self.value = token.value
        self.line = token.line
        self.program = token.program

    def __repr__(self):
        return f"(String: {self.value})"


class Identifier:
    def __init__(self, token):
        self.start = token.start
        self.value = token.value
        self.line = token.line
        self.program = token.program

    def __repr__(self):
        return f"(Identifier: {self.value})"
