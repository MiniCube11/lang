from lexer import Lexer
from _parser import Parser
from interpreter import Interpreter
import errors as er

def run_program(program):
    try:
        lexer = Lexer()
        tokens = lexer.get_tokens(program)
        parser = Parser()
        parse_result = parser.parse(tokens)
        interpreter = Interpreter()
        result = interpreter.interpret(parse_result)
        print(result)
    except Exception as e:
        er.print_error(e)
    except Exception as e:
        raise Exception

while True:
    program = input("> ")
    run_program(program)