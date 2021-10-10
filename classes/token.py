class Token:
    def __init__(self, start, length, line, program, token_type, value=None):
        self.start = start
        self.length = length
        self.token_type = token_type
        self.value = value
        self.line = line
        self.program = program

    def __repr__(self):
        return f"({self.token_type} {self.value})"