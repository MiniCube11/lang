import sys
import argparse

from lang.lexer import Lexer
from lang.parser import Parser
from lang.interpreter import Interpreter
from classes.environment import Environment
import classes.errors as er
import settings

environment = Environment()

lexer = Lexer()
parser = Parser()
interpreter = Interpreter(environment)


def run_program(program):
    try:
        tokens = lexer.get_tokens(program)
        parse_result = parser.parse(tokens)
        result = interpreter.interpret(parse_result)
        if settings.DEBUG:
            print(tokens)
            print(parse_result)
        print(*result, sep='\n')
    except Exception as e:
        er.print_error(e)
    except Exception as e:
        raise Exception


if len(sys.argv) == 2:
    with open(sys.argv[1], "r") as f:
        lines = f.readlines()
        program = ''.join(lines)
        run_program(program)
else:
    while True:
        program = input(">>> ")
        run_program(program)
