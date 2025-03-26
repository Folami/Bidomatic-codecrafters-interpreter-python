class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def __str__(self):
        # Use self.type.name so that "NUMBER" is printed instead of "TokenType.NUMBER".
        literal_str = str(self.literal) if self.literal is not None else ""
        return f"{self.type.name} {self.lexeme} {literal_str}".strip()