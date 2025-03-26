import sys
from app.scanner import Scanner

class PyLox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False
        

    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)
        self.had_error = True

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
    else:
        print("EOF  null") # Placeholder, remove this line when implementing the scanner
        

if __name__ == "__main__":
    main()