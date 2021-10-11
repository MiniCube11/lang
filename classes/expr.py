class AssignExpr:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return f"(Assign: {self.name} {self.value})"


class Expr:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(Expr: {self.left} {self.operator} {self.right})"


class UnaryExpr:
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"(Unary: {self.operator} {self.right})"
