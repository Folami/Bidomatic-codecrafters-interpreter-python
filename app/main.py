import sys
from app.scanner import Scanner
from app.parser import Parser
from app.ast_printer import AstPrinter
from app.token_type import TokenType
from app.interpreter import Interpreter


class PyLox:
    # A static interpreter reused across calls.
    interpreter = Interpreter()

    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

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
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
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
        scanner = Scanner(file_contents, lox)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
        if lox.had_error:
            exit(65)
    elif command == "parse":
        scanner = Scanner(file_contents, lox)
        tokens = scanner.scan_tokens()
        if lox.had_error:
            exit(65)
        parser = Parser(tokens, lox)
        expression = parser.parse()
        if lox.had_error:
            exit(65)
        print(AstPrinter().print(expression))
    elif command == "evaluate":
        scanner = Scanner(file_contents, lox)
        tokens = scanner.scan_tokens()
        if lox.had_error:
            exit(65)
        parser = Parser(tokens, lox)
        expression = parser.parse()
        if lox.had_error:
            exit(65)
        try:
            value = lox.interpreter.interpret(expression)
            print(lox.interpreter.stringify(value))
        except RuntimeError as error:
            lox.runtime_error(error)
    
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner
        

if __name__ == "__main__":
    main()