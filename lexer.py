import token_types as tt
import errors as er
from token import Token


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
        tokens.append(Token(self.curr, 1, self.line, self.program, "EOF"))
        return tokens

    def get_next_token(self):
        curr_char = self.program[self.curr]
        while curr_char == ' ':
            self.advance()
            if self.at_end():
                return None
            curr_char = self.program[self.curr]
        if curr_char in tt.SINGLE_CHAR_TOKENS:
            self.advance()
            return Token(self.curr - 1, 1, self.line, self.program, tt.SINGLE_CHAR_TOKENS[curr_char])
        if curr_char.isdigit():
            return self.get_number()
        raise er._SyntaxError(self.program, self.curr, self.line)

    def get_number(self):
        number = ""
        curr_char = self.program[self.curr]
        while curr_char.isdigit():
            number += curr_char
            self.advance()
            if self.at_end():
                break
            curr_char = self.program[self.curr]
        return Token(self.curr - len(number), len(number), self.line, self.program, "NUMBER", number)

    def advance(self):
        self.curr += 1

    def at_end(self):
        return self.curr >= len(self.program)
