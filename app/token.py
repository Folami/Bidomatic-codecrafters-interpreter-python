class Token:
    def __init__(self, type, lexeme, literal, line):
        self.type = type          # e.g. TokenType.NUMBER or TokenType.EOF
        self.lexeme = lexeme      # the string from the source code ("" for EOF)
        self.literal = literal    # e.g. 11.0 or None (for EOF)
        self.line = line

    def __str__(self):
        literal_str = str(self.literal) if self.literal is not None else "null"
        # When lexeme is empty (as for EOF), this produces: "EOF  null"
        return f"{self.type.name} {self.lexeme} {literal_str}".strip()
