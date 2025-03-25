import sys
from scanner import Scanner

class PyLox:
    def __init__(self):
        self.had_error = False
        self.had_runtime_error = False

    def run_file(self, path: str) -> None:
        try:
            with open(path, 'r') as f:
                source = f.read()
            self.run(source)
            if self.had_error:
                sys.exit(65)
            if self.had_runtime_error:
                sys.exit(70)
        except FileNotFoundError:
            print(f"Could not open file: {path}", file=sys.stderr)
            sys.exit(1)

    def run_prompt(self) -> None:
        try:
            while True:
                line = input("> ")
                if not line:
                    break
                self.run(line)
                self.had_error = False  # Reset error flag for each line
        except KeyboardInterrupt:
            print("\nExiting prompt.")

    def run(self, source: str) -> None:
        scanner = Scanner(source, self)
        tokens = scanner.scan_tokens()

        for token in tokens:
            print(token)

    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)
        self.had_error = True

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error{where}: {message}", file=sys.stderr)
        self.had_error = True

    def runtime_error(self, error) -> None:
        print(f"{error.message}\n[line {error.token.line}]", file=sys.stderr)
        self.had_runtime_error = True



