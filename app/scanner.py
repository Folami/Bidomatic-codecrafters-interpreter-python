import sys
from app.token_type import TokenType
from app.token import Token

class Scanner:
    def __init__(self, source: str, lox):
        self.source = source
        self.lox = lox
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1
        self.keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }


    def scan_tokens(self):
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self):
        return self.current >= len(self.source)

    def scan_token(self):
        c = self.advance()
        match c:
            # Single-character tokens.
            case '(' | ')' | '{' | '}' | ',' | '.' | '-' | '+' | ';' | '*':
                self.handle_single_character_token(c)
            # One-or-two character tokens.
            case '!' | '=' | '<' | '>':
                self.handle_one_or_two_character_token(c)
            # Ternary operator tokens.
            case '?' | ':':
                self.add_token(TokenType.QUESTION if c == '?' else TokenType.COLON)
            # Slash token and comments.
            case '/':
                self.handle_slash_token()
            # Ignore whitespace.
            case ' ' | '\r' | '\t':
                pass
            # Newline token.
            case '\n':
                self.line += 1
            # Literal tokens.
            case '"':
                self.string()
            case _:
                if c.isdigit():
                    self.number()
                elif c.isalpha() or c == '_':
                    self.identifier()
                else:
                    self.lox.error(self.line, f"Unexpected character: {c}")

    def handle_single_character_token(self, c):
        if c == '(':
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ')':
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == '{':
            self.add_token(TokenType.LEFT_BRACE)
        elif c == '}':
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ',':
            self.add_token(TokenType.COMMA)
        elif c == '.':
            self.add_token(TokenType.DOT)
        elif c == '-':
            self.add_token(TokenType.MINUS)
        elif c == '+':
            self.add_token(TokenType.PLUS)
        elif c == ';':
            self.add_token(TokenType.SEMICOLON)
        elif c == '*':
            self.add_token(TokenType.STAR)

    def handle_one_or_two_character_token(self, c):
        if c == '!':
            self.add_token(TokenType.BANG_EQUAL if self.match('=') else TokenType.BANG)
        elif c == '=':
            self.add_token(TokenType.EQUAL_EQUAL if self.match('=') else TokenType.EQUAL)
        elif c == '<':
            self.add_token(TokenType.LESS_EQUAL if self.match('=') else TokenType.LESS)
        elif c == '>':
            self.add_token(TokenType.GREATER_EQUAL if self.match('=') else TokenType.GREATER)

    def handle_slash_token(self):
        if self.match('/'):
            # A comment goes until the end of the line.
            while self.peek() != '\n' and not self.is_at_end():
                self.advance()
        elif self.match('*'):
            # A block comment.
            while self.peek() != '*' and self.peek_next() != '/' and not self.is_at_end():
                if self.peek() == '\n':
                    self.line += 1
                self.advance()
        else:
            self.add_token(TokenType.SLASH)

    def advance(self):
        self.current += 1
        return self.source[self.current - 1]

    def add_token(self, type, literal=None):
        text = self.source[self.start : self.current]
        token = Token(type, text, literal, self.line)
        self.tokens.append(token)

    def match(self, expected):
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True
    
    def peek(self):
        if self.is_at_end():
            return '\0'
        return self.source[self.current]

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.is_at_end():
            self.lox.error(self.line, "Unterminated string.")
            return
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()
        if self.peek() == '.' and self.peek_next().isdigit():
            # Consume the "."
            self.advance()
            while self.peek().isdigit():
                self.advance()
        number = self.source[self.start : self.current]
        self.add_token(TokenType.NUMBER, float(number))

    def peek_next(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current + 1]

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start : self.current]
        type = self.keywords.get(text)
        if type is None:
            type = TokenType.IDENTIFIER
        self.add_token(type)

