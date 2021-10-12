import lang.token_types as tt
import classes.errors as er
from classes.token import Token


class Lexer:
    def get_tokens(self, program):
        self.program = program
        self.line = 1
        self.curr = 0
        self.had_error = False
        tokens = []
        while not self.at_end():
            token = self.get_next_token()
            if token:
                tokens.append(token)
        tokens.append(Token(self.curr, 1, self.line, self.program, tt.C_EOF))
        return tokens

    def get_next_token(self):
        curr_char = self.program[self.curr]
        while curr_char == ' ':
            self.advance()
            if self.at_end():
                return None
            curr_char = self.program[self.curr]
        if curr_char == tt.NEWLINE:
            self.advance()
            return Token(self.curr - 1, 1, self.line, self.program, tt.C_EOF)
        if curr_char in tt.SINGLE_CHAR_TOKENS:
            self.advance()
            return Token(self.curr - 1, 1, self.line, self.program, tt.SINGLE_CHAR_TOKENS[curr_char])
        if curr_char in tt.COMP_OPERATORS or curr_char == tt.EQUAL:
            return self.get_comp_operator()
        if curr_char in tt.BOOL_OPERATOR_CHARS:
            return self.get_bool_operator()
        if curr_char.isdigit():
            return self.get_number()
        if curr_char == tt.QUOTATION:
            return self.get_string()
        if self.is_identifier_char(curr_char):
            return self.get_identifier()
        raise er._SyntaxError(self.program, self.curr, self.line)

    def get_comp_operator(self):
        curr_char = self.program[self.curr]
        operator = curr_char
        self.advance()
        if self.at_end():
            if operator == tt.EQUAL:
                return Token(self.curr, 1, self.line, self.program, tt.C_EQUAL)
            return Token(self.curr, 1, self.line, self.program, tt.COMP_OPERATORS[operator])
        curr_char = self.program[self.curr]
        if curr_char == tt.EQUAL:
            self.advance()
            return Token(self.curr - 2, 2, self.line, self.program, tt.COMP_OPERATORS[operator + curr_char])
        if operator == tt.EQUAL:
            return Token(self.curr, 1, self.line, self.program, tt.C_EQUAL)
        return Token(self.curr, 1, self.line, self.program, tt.COMP_OPERATORS[operator])

    def get_bool_operator(self):
        first_char = self.program[self.curr]
        self.advance()
        if self.at_end() or self.program[self.curr] != first_char:
            raise er._SyntaxError(self.program, self.curr, self.line)
        operator = first_char + first_char
        self.advance()
        return Token(self.curr - 2, 1, self.line, self.program, tt.BOOL_OPERATORS[operator])

    def get_number(self):
        number = ""
        curr_char = self.program[self.curr]
        while curr_char.isdigit():
            number += curr_char
            self.advance()
            if self.at_end():
                break
            curr_char = self.program[self.curr]
        if curr_char.isalpha():
            raise er._SyntaxError(self.program, self.curr, self.line)
        return Token(self.curr - len(number), len(number), self.line, self.program, tt.C_NUMBER, number)

    def get_string(self):
        string = ""
        self.advance()
        if self.at_end():
            raise er._SyntaxError(self.program, self.curr, self.line)
        curr_char = self.program[self.curr]
        while curr_char != '"':
            string += curr_char
            self.advance()
            if self.at_end():
                raise er._SyntaxError(self.program, self.curr, self.line)
            curr_char = self.program[self.curr]
        self.advance()
        return Token(self.curr - len(string), len(string), self.line, self.program, tt.C_STRING, string)

    def get_identifier(self):
        identifier = ""
        curr_char = self.program[self.curr]
        while self.is_identifier_char(curr_char) or curr_char.isdigit():
            identifier += curr_char
            self.advance()
            if self.at_end():
                break
            curr_char = self.program[self.curr]
        if identifier in tt.KEYWORDS:
            return Token(self.curr - len(identifier), len(identifier), self.line, self.program, tt.C_KEYWORD, tt.KEYWORDS[identifier])
        return Token(self.curr - len(identifier), len(identifier), self.line, self.program, tt.C_IDENTIFIER, identifier)

    def is_identifier_char(self, char):
        return char.isalpha() or char == '_'

    def advance(self):
        self.curr += 1

    def at_end(self):
        return self.curr >= len(self.program)
