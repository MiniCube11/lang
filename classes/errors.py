class _SyntaxError(Exception):
    def __init__(self, program, curr, line):
        self.program = program
        self.curr = curr
        self.line = line

class _ParseError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

class _RuntimeError(Exception):
    def __init__(self, message, token):
        self.message = message
        self.token = token

class _Error(Exception):
    def __init__(self, message):
        self.message = message
        

def print_error(error):
    message = None
    if isinstance(error, _SyntaxError):
        message = f"{error.program}\n"
        message += f"{' '*error.curr}^\n"
        message += f"SyntaxError: Invalid Syntax (line {error.line})"
    elif isinstance(error, _ParseError):
        message = f"{error.token.program}\n"
        message += f"{' '*error.token.start}^\n"
        message += f"SyntaxError: Invalid Syntax (line {error.token.line})\n"
        message += error.message
    elif isinstance(error, _RuntimeError):
        message = f"{error.token.program}\n"
        message += f"RuntimeError: {error.message} (line {error.token.line})\n"
    if message:
        print(message)
    else:
        raise error