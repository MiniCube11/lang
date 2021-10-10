import lang.token_types as tt
import classes.errors as er
from classes.expr import Expr, UnaryExpr
from classes.token import Token
from classes.datatypes import Number


class Interpreter:
    def interpret(self, expression):
        result = self.evaluate(expression)
        if result is True:
            return "true"
        if result is False:
            return "false"
        return result

    def evaluate(self, expression):
        if isinstance(expression, Expr):
            return self.ev_expr(expression)
        if isinstance(expression, UnaryExpr):
            return self.ev_unary_expr(expression)
        if isinstance(expression, Number):
            return int(expression.value)

    def ev_expr(self, expression):
        operator = expression.operator.token_type
        left = self.evaluate(expression.left)
        right = self.evaluate(expression.right)
        if operator == tt.C_OR:
            return bool(left or right)
        if operator == tt.C_AND:
            return bool(left and right)
        if operator == tt.C_EQEQUAL:
            return bool(left == right)
        if operator == tt.C_GREATERTHAN:
            return bool(left > right)
        if operator == tt.C_LESSTHAN:
            return bool(left < right)
        if operator == tt.C_GREATEREQUAL:
            return bool(left >= right)
        if operator == tt.C_LESSEQUAL:
            return bool(left <= right)
        if operator == tt.C_PLUS:
            return left + right
        if operator == tt.C_MINUS:
            return left - right
        if operator == tt.C_MUL:
            return left * right
        if operator == tt.C_DIV:
            if right == 0:
                raise er._RuntimeError("Division by zero", expression.operator)
            return left / right

    def ev_unary_expr(self, expression):
        if expression.operator.token_type == tt.C_MINUS:
            return -self.evaluate(expression.right)
