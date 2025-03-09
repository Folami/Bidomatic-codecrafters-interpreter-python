import sys
from typing import Tuple

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.index = 0
        self.line = 1
        self.has_error = False

    def scan_tokens(self) -> None:
        """Main scanning loop"""
        while self.index < len(self.source):
            c = self.source[self.index]
            
            if self._handle_whitespace(c):
                continue
                
            if self._handle_comments_and_division(c):
                continue
                
            if self._handle_string_literal(c):
                continue
                
            if self._handle_number_literal(c):
                continue
                
            if self._handle_basic_tokens(c):
                continue
                
            if self._handle_operators():
                continue
                
            self._report_error(c)

        print("EOF  null")
        return self.has_error

    def _handle_string_literal(self, c: str) -> bool:
        """Handle string literals enclosed in double quotes"""
        if c != '"':
            return False
            
        self.index += 1  # Skip opening quote
        string_content = []
        unterminated = True
        
        while self.index < len(self.source):
            ch = self.source[self.index]
            if ch == '"':
                unterminated = False
                break
            if ch == '\n':
                self.line += 1
            string_content.append(ch)
            self.index += 1
            
        if unterminated:
            print(f"[line {self.line}] Error: Unterminated string.", file=sys.stderr)
            self.has_error = True
        else:
            content = "".join(string_content)
            print(f'STRING "{content}" {content}')
            self.index += 1  # Skip closing quote
            
        return True

    def _handle_number_literal(self, c: str) -> bool:
        """Handle number literals"""
        if not c.isdigit():
            return False
        
        number_content = []
        while self.index < len(self.source) and self.source[self.index].isdigit():
            number_content.append(self.source[self.index])
            self.index += 1
        
        # Handle fractional part
        if self.index < len(self.source) and self.source[self.index] == '.':
            number_content.append('.')
            self.index += 1
            while self.index < len(self.source) and self.source[self.index].isdigit():
                number_content.append(self.source[self.index])
                self.index += 1
        
        content = "".join(number_content)
        if '.' not in content:
            content += '.0'
        print(f'NUMBER {content} {content}')
        return True

    def _handle_whitespace(self, c: str) -> bool:
        """Handle whitespace characters including newlines"""
        if c == '\n':
            self.line += 1
            self.index += 1
            return True
        if c.isspace():
            self.index += 1
            return True
        return False

    def _handle_comments_and_division(self, c: str) -> bool:
        """Handle comments starting with // and division operator /"""
        if c != '/':
            return False
            
        if self.index + 1 < len(self.source) and self.source[self.index + 1] == '/':
            # Skip comment until end of line
            while self.index < len(self.source) and self.source[self.index] != '\n':
                self.index += 1
            return True
        
        # Single slash for division
        print("SLASH / null")
        self.index += 1
        return True

    def _handle_basic_tokens(self, c: str) -> bool:
        """Handle single-character tokens"""
        tokens = {
            '(': 'LEFT_PAREN',
            ')': 'RIGHT_PAREN',
            '{': 'LEFT_BRACE',
            '}': 'RIGHT_BRACE',
            ',': 'COMMA',
            '.': 'DOT',
            '-': 'MINUS',
            '+': 'PLUS',
            ';': 'SEMICOLON',
            '*': 'STAR'
        }
        if c in tokens:
            print(f"{tokens[c]} {c} null")
            self.index += 1
            return True
        return False

    def _handle_operators(self) -> bool:
        """Handle single and two-character operators"""
        if self.index + 1 >= len(self.source):
            return self._handle_single_operator()
            
        # Try two-character operators first
        two_char = self.source[self.index:self.index + 2]
        two_char_ops = {
            '<=': 'LESS_EQUAL',
            '>=': 'GREATER_EQUAL',
            '==': 'EQUAL_EQUAL',
            '!=': 'BANG_EQUAL'
        }
        
        if two_char in two_char_ops:
            print(f"{two_char_ops[two_char]} {two_char} null")
            self.index += 2
            return True
            
        return self._handle_single_operator()

    def _handle_single_operator(self) -> bool:
        """Handle single-character operators"""
        c = self.source[self.index]
        operators = {
            '<': 'LESS',
            '>': 'GREATER',
            '=': 'EQUAL',
            '!': 'BANG'
        }
        
        if c in operators:
            print(f"{operators[c]} {c} null")
            self.index += 1
            return True
        return False

    def _report_error(self, c: str) -> None:
        """Report unexpected character errors"""
        print(f"[line {self.line}] Error: Unexpected character: {c}", file=sys.stderr)
        self.has_error = True
        self.index += 1


def main():
    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command, filename = sys.argv[1:3]
    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    try:
        with open(filename) as file:
            source = file.read()
    except IOError as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        exit(1)

    print("Logs from your program will appear here!", file=sys.stderr)
    
    scanner = Scanner(source)
    has_error = scanner.scan_tokens()
    exit(65 if has_error else 0)


if __name__ == "__main__":
    main()

