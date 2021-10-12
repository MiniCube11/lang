class IfStmt:
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __repr__(self):
        return f"(IF {self.condition} {self.statements})"
