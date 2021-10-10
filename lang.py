from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter
import classes.errors as er


def run_program(program):
    try:
        lexer = Lexer()
        tokens = lexer.get_tokens(program)
        print(tokens)
        # parser = Parser()
        # parse_result = parser.parse(tokens)
        # interpreter = Interpreter()
        # result = interpreter.interpret(parse_result)
        # print(result)
    except Exception as e:
        er.print_error(e)
    except Exception as e:
        raise Exception


while True:
    program = input("> ")
    run_program(program)
