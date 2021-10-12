import grammar.token_types as tt
import classes.errors as er
from classes.stmt import IfStmt, WhileStmt
from classes.expr import AssignExpr, Expr, UnaryExpr
from classes.token import Token
from classes.datatypes import Number, String, Identifier


class Interpreter:
    def __init__(self, environment):
        self.environment = environment

    def interpret(self, statements):
        results = []
        for stmt in statements:
            interpret_res = self.interpret_expr(stmt)
            if isinstance(interpret_res, list):
                for value in interpret_res:
                    results.append(self.format_value(value))
            else:
                results.append(interpret_res)
        return results

    def format_value(self, value):
        if value is True:
            return "true"
        if value is False:
            return "false"
        return value

    def interpret_expr(self, expression):
        result = self.evaluate(expression)
        return self.format_value(result)

    def evaluate(self, expression):
        if isinstance(expression, IfStmt):
            return self.ev_if_stmt(expression)
        if isinstance(expression, WhileStmt):
            return self.ev_while_stmt(expression)
        if isinstance(expression, AssignExpr):
            return self.ev_assignment(expression)
        if isinstance(expression, Expr):
            return self.ev_expr(expression)
        if isinstance(expression, UnaryExpr):
            return self.ev_unary_expr(expression)
        if isinstance(expression, Number):
            return int(expression.value)
        if isinstance(expression, String):
            return expression.value
        if isinstance(expression, Identifier):
            return self.ev_identifier(expression)

    def ev_if_stmt(self, expression):
        if self.evaluate(expression.condition):
            result = []
            for stmt in expression.statements:
                if res := self.evaluate(stmt):
                    result.append(res)
            return result

    def ev_while_stmt(self, expression):
        result = []
        while self.evaluate(expression.condition):
            for stmt in expression.statements:
                if res := self.evaluate(stmt):
                    result.append(res)
        return result

    def ev_assignment(self, expression):
        name = expression.name
        value = self.evaluate(expression.value)
        self.environment.assign(name, value)
        return value

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

    def ev_identifier(self, expression):
        value = self.environment.get(expression)
        return value
