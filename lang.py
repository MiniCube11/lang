import sys
import argparse

from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter
from classes.environment import Environment
import classes.errors as er

environment = Environment()

lexer = Lexer()
parser = Parser()
interpreter = Interpreter(environment)

argparser = argparse.ArgumentParser()
argparser.add_argument("--debug", "-d", type=bool, default=False)
args, uknownargs = argparser.parse_known_args()


def run_program(program, repl=False, debug_mode=False):
    try:
        tokens = lexer.get_tokens(program)
        if debug_mode:
            print(tokens)

        parse_result = parser.parse(tokens)
        if debug_mode:
            print(parse_result)

        results, printed_results = interpreter.interpret(parse_result)
        if not repl:
            results = printed_results
        print(*results, sep='\n')

    except Exception as e:
        er.print_error(e)
    except Exception as e:
        raise Exception


if len(sys.argv) >= 2:
    filename = sys.argv[1]
    with open(filename, "r") as f:
        lines = f.readlines()
        program = ''.join(lines)
        run_program(program, debug_mode=args.debug)
else:
    while True:
        program = input(">>> ")
        run_program(program, repl=True)
