import sys
from typing import TYPE_CHECKING
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter
from app.token_type import TokenType
from app.interpreter import Interpreter
from app.runtime_error import RuntimeError

try:
    from app.resolver import Resolver
except ImportError:
    Resolver = None  # or define a dummy Resolver if needed

if TYPE_CHECKING:
    pass  # TYPE_CHECKING block can be left empty or used for type hints only


class PyLox:
    # A static interpreter reused across calls.
    interpreter = Interpreter()
    # A static instance of the PyLox class.
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def runScanner(self, source: str):
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()
        return tokens
        # Placeholder for the scanner's output

    def runParser(self, source: str):
        tokens = self.runScanner(source)
        parser = Parser(tokens, self)
        expression = parser.parseExpression()
        if self.had_error:
            exit(65)
        return expression
    
    def runInterpreter(self, source: str):
        expression = self.runParser(source)
        if self.had_error:
            exit(65)
        self.interpreter.interpretExpression(expression)
        
    def runResolver(self, statements):
        if statements is not None:
            resolver = Resolver(self.interpreter)
            resolver.set_lox(self)  # Pass PyLox instance to resolver
            resolver.resolve(statements)
        return statements

    def runPyLox(self, source: str):
        tokens = self.runScanner(source)
        parser = Parser(tokens, self)
        statements = parser.parseStatements()
        if self.had_error:
            exit(65)
        statements = self.runResolver(statements)
        if self.had_error:
            exit(65)
        try:
            self.interpreter.interpretStatements(statements)
        except RuntimeError as error:
            self.runtime_error(error)
            exit(70)  # Exit with code 70 for runtime errors

    def error(self, token_or_line, message: str) -> None:
        # If token_or_line is an int, treat it as a line number
        if isinstance(token_or_line, int):
            self.report(token_or_line, "", message)
        else:
            # Otherwise, assume it's a token
            if token_or_line.type == TokenType.EOF:
                self.report(token_or_line.line, " at end", message)
            else:
                self.report(token_or_line.line, 
                    f" at '{token_or_line.lexeme}'", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.had_error = True

    def runtime_error(self, error) -> None:
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True

    def run(self):
        # This method should be called to start the program
        lox = PyLox()
        if len(sys.argv) < 3:
            print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
            exit(1)

        command = sys.argv[1]
        filename = sys.argv[2]
        with open(filename) as file:
            file_contents = file.read()

        if command == "tokenize":
            # Tokenize the input using the scanner.
            tokens = lox.runScanner(file_contents)
            # Print the tokens.
            for token in tokens:
                print(token)
            if lox.had_error:
                exit(65)

        elif command == "parse":
            # Parse the expression using the parser.
            expression = lox.runParser(file_contents)
            if lox.had_error:
                exit(65)
            print(AstPrinter().print(expression))

        elif command == "evaluate":
            # Evaluate the expression using the interpreter.
            try:
                lox.runInterpreter(file_contents)
            except RuntimeError as error:
                lox.runtime_error(error)
                exit(70)

        elif command == "resolve":
            # Resolve the expression using the resolver.
            try:
                tokens = lox.runScanner(file_contents)
                parser = Parser(tokens, lox)
                statements = parser.parseStatements()
                if lox.had_error:
                    exit(65)
                lox.runResolver(statements)
            except RuntimeError as error:
                lox.runtime_error(error)
                exit(70)

        elif command == "run":
            # Run the interpreter on the provided source code.
            try:
                lox.runPyLox(file_contents)
            except RuntimeError as error:
                lox.runtime_error(error)
                exit(70)

        else:
            print("EOF  null")
            exit(0)

if __name__ == "__main__":
    py_lox = PyLox()
    py_lox.run()