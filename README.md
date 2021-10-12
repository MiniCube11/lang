# Lang

A toy interpreted programming language written in Python.

_The language is incomplete. There are currently no print statements so all expressions are printed, which may make the output a bit messy._

## Run this project

Make sure you have the latest Python version installed.

Running `lang.py` will open up an interactive repl.

```
python lang.py
```

To run a file:

```
python lang.py <name-of-file>
```

## Syntax

```
1 + 1
3 - 2 * -6 / 3
(1 + 1) * 3
```

Expressions follow normal BEDMAS rules.

```
1 == 2
1 == 1 && 3 >= 0
```

Logical and comparison operators follow the C-style syntax.

```
a = 1
a = a + 3
1 + b = 1
```

Variables can be used once they have been assigned a value. Variable assignments are treated as expressions and can be used in arithmetic expressions.

```
if (a == 1) {
    b = 1
}

while (a < 10) {
    a = a + 1
}
```

If statements and while loops follow C-style syntax.

## Project Structure

`lang.py` - The file that imports the modules for reading in the program source and printing out the results of the program.

## lang

The module responsible for lexing, parsing, and interpreting the program.

`lexer.py` - Scans the program for tokens.

`parser.py` - Parses through the tokens and returns a list of statements.

`interpreter.py` - Executes each of the statements.

## classes

The files that contain the classes which are used in the module `lang` for executing the program.

## grammar

The files that contain information related to the language's grammar.

`token_types.py` - Stores the information of all the token types in language.
