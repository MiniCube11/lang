import classes.errors as er


class Environment:
    def __init__(self):
        self.variables = {}

    def assign(self, name, value):
        self.variables[name] = value

    def get(self, token):
        if token.value in self.variables:
            return self.variables[token.value]
        raise er._RuntimeError(f"Name '{token.value}' is not defined.", token)
