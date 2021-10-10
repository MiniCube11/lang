from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter
import classes.errors as er
import settings

lexer = Lexer()
parser = Parser()
interpreter = Interpreter()


def run_program(program):
    try:
        tokens = lexer.get_tokens(program)
        parse_result = parser.parse(tokens)
        result = interpreter.interpret(parse_result)
        if settings.DEBUG:
            print(tokens)
            print(parse_result)
        print(result)
    except Exception as e:
        er.print_error(e)
    except Exception as e:
        raise Exception


while True:
    program = input("> ")
    run_program(program)
