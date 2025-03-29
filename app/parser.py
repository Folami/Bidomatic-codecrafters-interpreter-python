from typing import List
from app.token import Token
from app.token_type import TokenType
from app.expr import Literal, Grouping, Unary, Binary, Comma, Conditional, Variable
from app.stmt import Print, Expression, Var, Assign, Block



class Parser:
    def __init__(self, tokens: List[Token], lox):
        self.lox = lox
        self.tokens = tokens
        self.current = 0

    class ParserError(Exception):
        pass

    def parseExpression(self):
        # This method is a wrapper to handle parsing errors.
        try:
            return self.expression()
        except Parser.ParserError:
            return None
        # Handle parser errors here if needed.

    def parseStatements(self):
        statements = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def expression(self):
        # return self.equality()
        # return self.conditional()
        return assignment()
    
    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except Parser.ParserError:
            self.synchronize()
            return None
    
    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        return self.expression_statement()
    
    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)
    
    def var_declaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)
    
    def expression_statement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Expression(expr)
    
    def block(self):
        statements = []
        while not self.is_at_end() and not self.check(TokenType.RIGHT_BRACE):
            statements.append(self.declaration())
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements
    
    def assignment(self):
        expr = self.conditional()
        if self.match(TokenType.EQUAL):
            equals = self.previous()
            value = self.assignment()
            if isinstance(expr, Variable):
                name = expr.name
                return Assign(name, value)
            self.error(equals, "Invalid assignment target.")
        return expr

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
        if self.match(TokenType.IDENTIFIER):
            return Variable(self.previous())
        if self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expect expression.")
        
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
        return self.ParserError()
    
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
