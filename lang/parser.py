from collections import deque
import lang.token_types as tt
import classes.errors as er
from classes.expr import AssignExpr, Expr, UnaryExpr
from classes.datatypes import Number, String, Identifier


class Parser:
    def parse(self, tokens):
        return self.expression(tokens[:-1])

    def expression(self, tokens):
        tokens = self.remove_brackets(tokens)
        return self.assign_expr(tokens)

    def assign_expr(self, tokens):
        if len(tokens) > 1:
            if res := self.match(tokens[1], tt.C_EQUAL):
                if tokens[0].token_type != tt.C_IDENTIFIER:
                    raise er._ParseError(
                        f"Expect name before '{tt.EQUAL}'.", tokens[0])
                if len(tokens) == 2:
                    raise er._ParseError(
                        f"Expect expression after '{tt.EQUAL}'.", tokens[1])
                return AssignExpr(tokens[0], self.expression(tokens[2:]))
        return self.or_expr(tokens)

    def or_expr(self, tokens):
        if res := self.find_expr(tokens, tt.C_OR):
            return res
        return self.and_expr(tokens)

    def and_expr(self, tokens):
        if res := self.find_expr(tokens, tt.C_AND):
            return res
        return self.compare_equals_expr(tokens)

    def compare_equals_expr(self, tokens):
        if res := self.find_expr(tokens, *list(tt.COMP_OPERATORS.values())):
            return res
        return self.plus_minus_expr(tokens)

    def plus_minus_expr(self, tokens):
        if res := self.find_expr(tokens, tt.C_PLUS, tt.C_MINUS, check_unary=True):
            return res
        return self.mul_div_expr(tokens)

    def mul_div_expr(self, tokens):
        if res := self.find_expr(tokens, tt.C_MUL, tt.C_DIV):
            return res
        return self.unary_expr(tokens)

    def unary_expr(self, tokens):
        if res := self.match(tokens[0], tt.C_MINUS):
            return UnaryExpr(res, self.expression(tokens[1:]))
        return self.single_token(tokens)

    def single_token(self, tokens):
        token = tokens[0]
        if len(tokens) == 1:
            if token.token_type == tt.C_NUMBER:
                return Number(token)
            if token.token_type == tt.C_STRING:
                return String(token)
            if token.token_type == tt.C_IDENTIFIER:
                return Identifier(token)
        raise er._SyntaxError(token.program, token.start, token.line)

    def new_expr(self, tokens, i, operator):
        symbol = tokens[i].program[tokens[i].start]
        if i == 0:
            message = f"Expected expression before '{symbol}'."
            raise er._ParseError(message, tokens[i])
        if i == len(tokens) - 1:
            message = f"Expected expression after '{symbol}'."
            raise er._ParseError(message, tokens[i])
        return Expr(self.expression(tokens[:i]), operator, self.expression(tokens[i+1:]))

    def is_unary_operator(self, tokens, i):
        if i < 0 or self.match(tokens[i], *tt.C_OPERATORS):
            return True
        return False

    def find_expr(self, tokens, *match_tokens, check_unary=False):
        self.brackets = 0
        for i in range(self.skip_assign_expr(tokens), -1, -1):
            self.match_brackets(tokens[i])
            if self.brackets == 0 and (not check_unary or not self.is_unary_operator(tokens, i-1)):
                res = self.match(tokens[i], *match_tokens)
                if res:
                    return self.new_expr(tokens, i, res)
        self.check_brackets(tokens)

    def skip_assign_expr(self, tokens):
        self.brackets = 0
        self.last_equal = len(tokens)-1
        for i in range(len(tokens)-1, -1, -1):
            self.match_brackets(tokens[i])
            if self.brackets == 0 and self.match(tokens[i], tt.C_EQUAL):
                self.last_equal = i
        self.check_brackets(tokens)
        return self.last_equal

    def match(self, curr_token, *tokens):
        for token in tokens:
            if curr_token.token_type == token:
                return curr_token
        return None

    def match_brackets(self, token):
        if token.token_type == tt.C_LPAREN:
            self.brackets += 1
        elif token.token_type == tt.C_RPAREN:
            self.brackets -= 1

    def check_brackets(self, tokens):
        if self.brackets < 0:
            raise er._ParseError("Expect '(' before ')'.", tokens[-1])
        if self.brackets > 0:
            raise er._ParseError("Expect ')' after '('.", tokens[0])

    def remove_brackets(self, tokens):
        brackets_stack = deque()
        for i in range(len(tokens)):
            token = tokens[i]
            if token.token_type == tt.C_LPAREN:
                brackets_stack.append(i)
            if token.token_type == tt.C_RPAREN:
                if not brackets_stack:
                    return tokens
                opening = brackets_stack.pop()
                if opening == 0 and i == len(tokens) - 1:
                    if len(tokens) == 2:
                        raise er._ParseError(
                            "Expect expression inside parentheses.", tokens[-1])
                    return tokens[1:-1]
        return tokens
