class IfStmt:
    def __init__(self, condition, statements, else_statements=None):
        self.condition = condition
        self.statements = statements
        self.else_statements = else_statements

    def __repr__(self):
        return f"(IF {self.condition} {self.statements} {self.else_statements})"


class WhileStmt:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"(WHILE {self.condition} {self.statements})"


class PrintStmt:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"(PRINT {self.expression})"
