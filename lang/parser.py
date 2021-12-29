from collections import deque
import grammar.token_types as tt
import classes.errors as er
from classes.stmt import IfStmt, WhileStmt, PrintStmt
from classes.expr import AssignExpr, Expr, UnaryExpr
from classes.datatypes import Number, String, Identifier


class Parser:
    def parse(self, tokens):
        self.curr = 0
        return self.find_statements(tokens)

    def find_statements(self, tokens, end=None, lcurl=False):
        if not end:
            end = len(tokens)
        statements = []
        while self.curr < end:
            stmt = self.find_stmt(tokens, lcurl)
            if stmt:
                statements.append(stmt)
        return statements

    def find_stmt(self, tokens, lcurl=False):
        if tokens[self.curr].value == tt.C_IF:
            return self.if_stmt(tokens)
        if tokens[self.curr].value == tt.C_WHILE:
            return self.while_stmt(tokens)
        if tokens[self.curr].value == tt.C_PRINT:
            return self.print_stmt(tokens)
        end_token_index = self.end_token_index(self.curr, tokens, lcurl=lcurl)
        curr_tokens = tokens[self.curr:end_token_index]
        stmt = None
        if curr_tokens:
            stmt = self.expression(curr_tokens)
        self.advance(tokens, advance_by=end_token_index + 1 - self.curr)
        return stmt

    def end_token_index(self, curr, tokens, lcurl=False):
        for i in range(curr, len(tokens)):
            if self.match(tokens[i], tt.C_EOF) or (lcurl and self.match(tokens[i], tt.C_RCURL)):
                return i
        return len(tokens) - 1

    def if_stmt(self, tokens):
        condition = self.find_condition(tokens, tt.IF)
        statements = self.find_block_or_stmt(tokens, tt.IF)
        while self.curr < len(tokens) and self.match(tokens[self.curr], tt.C_EOF):
            self.advance(tokens)
        if self.curr >= len(tokens):
            return IfStmt(self.expression(condition), statements)
        else_statements = None
        if tokens[self.curr].value == tt.C_ELSE:
            self.advance(tokens)
            else_statements = self.find_block_or_stmt(tokens, tt.ELSE)
        return IfStmt(self.expression(condition), statements, else_statements)

    def while_stmt(self, tokens):
        condition = self.find_condition(tokens, tt.WHILE)
        statements = self.find_block_or_stmt(tokens, tt.WHILE)
        return WhileStmt(self.expression(condition), statements)

    def print_stmt(self, tokens):
        start_pos = self.curr
        while self.curr < len(tokens) and not self.match(tokens[self.curr], tt.C_EOF):
            self.advance(tokens)
        return PrintStmt(self.expression(tokens[start_pos+1:self.curr]))

    def find_condition(self, tokens, keyword):
        start_pos = self.curr
        res = self.match(tokens[start_pos+1], tt.C_LPAREN)
        if not res:
            raise er._ParseError(
                f"Expect '{tt.LPAREN}' after {keyword} keyword.", tokens[start_pos+1])
        self.brackets = 0
        self.advance(tokens)
        while self.curr < len(tokens):
            self.match_brackets(tokens[self.curr])
            if self.brackets == 0:
                break
            self.advance(tokens)
        condition = tokens[start_pos+2:self.curr]
        if not condition:
            raise er._ParseError(
                "Expect condition inside parentheses.", tokens[start_pos+1])
        self.advance(tokens)
        return condition

    def find_block(self, tokens):
        start_pos = self.curr
        while self.curr < len(tokens):
            if self.match(tokens[self.curr], tt.C_RCURL):
                break
            self.advance(tokens)
        if self.curr < len(tokens) and self.match(tokens[self.curr], tt.C_RCURL):
            end = self.curr
            self.advance(tokens, advance_by=start_pos + 1 - self.curr)
            statements = self.find_statements(tokens, end, lcurl=True)
            if not statements:
                raise er._ParseError(
                    f"Expect statements inside curly braces.", tokens[self.curr-1])
            self.advance(tokens)
            return statements
        else:
            raise er._ParseError(
                f"Expect '{tt.RCURL}' after '{tt.LCURL}'.", tokens[self.curr-1])

    def find_block_or_stmt(self, tokens, keyword):
        start_pos = self.curr - 1
        while self.curr < len(tokens) and self.match(tokens[self.curr], tt.C_EOF):
            self.advance(tokens)
        if self.curr >= len(tokens):
            raise er._ParseError(
                f"Expect a block or statement after '{keyword}''.", tokens[start_pos])
        if self.match(tokens[self.curr], tt.C_LCURL):
            return self.find_block(tokens)
        else:
            stmt = self.find_stmt(tokens)
            if not stmt:
                raise er._ParseError(
                    f"Expect expression after '{keyword}'.", tokens[self.curr-1])
            return [stmt]

    def expression(self, tokens):
        tokens = self.remove_brackets(tokens)
        return self.assign_expr(tokens)

    def assign_expr(self, tokens):
        if len(tokens) > 1:
            if self.match(tokens[1], tt.C_EQUAL):
                if tokens[0].token_type != tt.C_IDENTIFIER:
                    raise er._ParseError(
                        f"Expect name before '{tt.EQUAL}'.", tokens[0])
                if len(tokens) == 2:
                    raise er._ParseError(
                        f"Expect expression after '{tt.EQUAL}'.", tokens[1])
                return AssignExpr(tokens[0].value, self.expression(tokens[2:]))
        return self.or_expr(tokens)

    def or_expr(self, tokens):
        res = self.find_expr(tokens, tt.C_OR)
        if res:
            return res
        return self.and_expr(tokens)

    def and_expr(self, tokens):
        res = self.find_expr(tokens, tt.C_AND)
        if res:
            return res
        return self.compare_equals_expr(tokens)

    def compare_equals_expr(self, tokens):
        res = self.find_expr(tokens, *list(tt.COMP_OPERATORS.values()))
        if res:
            return res
        return self.plus_minus_expr(tokens)

    def plus_minus_expr(self, tokens):
        res = self.find_expr(tokens, tt.C_PLUS, tt.C_MINUS, check_unary=True)
        if res:
            return res
        return self.mul_div_expr(tokens)

    def mul_div_expr(self, tokens):
        res = self.find_expr(tokens, tt.C_MUL, tt.C_DIV)
        if res:
            return res
        return self.unary_expr(tokens)

    def unary_expr(self, tokens):
        res = self.match(tokens[0], tt.C_MINUS)
        if res:
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

    def advance(self, tokens, advance_by=1):
        if self.curr <= len(tokens) - advance_by:
            self.curr += advance_by
            return True
        return False

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
