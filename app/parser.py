from typing import List
from app.token import Token
from app.token_type import TokenType
from app.expr import Literal, Grouping, Unary, Binary

class Parser:
    def __init__(self, tokens: List[Token], lox):
        self.lox = lox
        self.tokens = tokens
        self.current = 0

    class ParserError(Exception):
        pass

    def expression(self):
        # return self.equaliy()
        return self.conditional()

    def conditional(self):
        # Start with a comma expression (the next-higher precedence)
        expr = self.comma()
        if self.match(TokenType.QUESTION):  # for "?"
            then_branch = self.expression()  # Parse the true branch
            self.consume(TokenType.COLON, "Expect ':' after expression.")
            else_branch = self.conditional() # Right associativity: recursively parse the else branch.
            expr = Conditional(expr, then_branch, else_branch)
        return expr

    def comma(self):
        expr = self.equality()
        while self.match(TokenType.COMMA):
            operator = self.previous()
            right = self.equality()
            expr = Comma(expr, operator, right)
        return expr
    
    def equality(self):
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr
    
    def comparison(self):
        expr = self.term()
        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        return expr
    
    def term(self):
        expr = self.factor()
        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        return expr
    
    def factor(self):
        expr = self.unary()
        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        return expr
    
    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
    
    def parse(self):
        try:
            return self.expression()
        except Parser.ParserError:
            return None
        # Handle parser errors here if needed.
        
    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def match(self, *types):
        for token_type in types:
            if self.check(token_type):
                self.advance()
                return True
        return False
    
    def check(self, token_type):
        if self.is_at_end():
            return False
        return self.peek().type == token_type
    
    def advance(self):
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def error(self, token, message):
        self.lox.error(token.line, message)
        return ParserError()
    
    def synchronize(self):
        self.advance()
        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return
            if self.peek().type in (
                TokenType.CLASS, 
                TokenType.FUN, 
                TokenType.VAR, 
                TokenType.FOR, 
                TokenType.IF, 
                TokenType.WHILE, 
                TokenType.PRINT, 
                TokenType.RETURN
            ):
                return
            self.advance()
