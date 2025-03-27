import sys
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter
from app.token_type import TokenType
from app.interpreter import Interpreter
from app.runtime_error import RuntimeError


class PyLox:
    # A static interpreter reused across calls.
    interpreter = Interpreter()
    # A static instance of the PyLox class.

    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def runScanner(self, source: str):
        scanner = Scanner(source, self)  # Use source instead of file_contents and pass self for lox
        tokens = scanner.scan_tokens()
        return tokens
        # Placeholder for the scanner's output

    def runParser(self, source: str):
        tokens = self.runScanner(source)
        parser = Parser(tokens, self)
        expression = parser.parse()  # Assign the result of parser.parse() to expression
        print(AstPrinter().print(expression))
        # Placeholder for the parser's output
        return expression
    
    def runInterpreter(self, source: str):
        tokens = self.runScanner(source)
        if self.had_error:
            exit(65)
        parser = Parser(tokens, self)
        expression = parser.parse()
        if self.had_error:
            exit(65)
        try:
            self.interpreter.interpret(expression)
        except RuntimeError as error:
            self.runtime_error(error)
            # Remove the raise error statement
            # raise error


    def error(self, token_or_line, message) -> None:
        # If token_or_line is an int, treat it as a line number.
        if isinstance(token_or_line, int):
            self.report(token_or_line, "", message)
        else:
            # Otherwise, assume it's a token.
            if token_or_line.type == TokenType.EOF:
                self.report(token_or_line.line, " at end", message)
            else:
                self.report(token_or_line.line, f" at '{token_or_line.lexeme}'", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.had_error = True

    def runtime_error(self, error) -> None:
        print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True

def main():
    lox = PyLox()
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]
    with open(filename) as file:
        file_contents = file.read()

    if command == "tokenize":
        tokens = lox.runScanner(file_contents)
        if lox.had_error:
            exit(65)
        for token in tokens:
            print(token)
    elif command == "parse":
        expression = lox.runParser(file_contents)
        if lox.had_error:
            exit(65)
        print(AstPrinter().print(expression))
    elif command == "evaluate":
        try:
            lox.runInterpreter(file_contents)
        except RuntimeError as error:
            lox.runtime_error(error)
            exit(70)
    
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner
        

if __name__ == "__main__":
    main()