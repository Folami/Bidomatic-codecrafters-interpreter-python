import time
from app.expr import Visitor
from app.runtime_error import RuntimeError
from app.token_type import TokenType
from app.return_exception import Return
from app.environment import Environment
from app.lox_callable import LoxCallable
from app.lox_function import LoxFunction
from app.lox_class import LoxClass
from app.lox_instance import LoxInstance

class Clock(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        # Return the current time in seconds.
        return time.time()

    def __str__(self):
        return "<native fn>"
    
class ReadInput(LoxCallable):
    def arity(self) -> int:
        return 0

    def call(self, interpreter, arguments):
        # Read a line from standard input and return it.
        return input()

    def __str__(self):
        return "<native fn>"
    
class ReadFile(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, arguments):
        # Read a file and return its contents.
        filename = arguments[0]
        with open(filename, 'r') as file:
            return file.read()

    def __str__(self):
        return "<native fn>"
    
class WriteFile(LoxCallable):
    def arity(self) -> int:
        return 2

    def call(self, interpreter, arguments):
        # Write to a file.
        filename = arguments[0]
        content = arguments[1]
        with open(filename, 'w') as file:
            file.write(content)
        return None

    def __str__(self):
        return "<native fn>"
    
class Print(LoxCallable):
    def arity(self) -> int:
        return 1

    def call(self, interpreter, arguments):
        # Print the argument to standard output.
        print(arguments[0])
        return None

    def __str__(self):
        return "<native fn>"

class Interpreter(Visitor):
    def __init__(self):
        self.globals = Environment()
        self.environment = self.globals
        self.locals = {}  # Dictionary to store resolved variables
        self.globals.define("clock", Clock())
    
    def interpretExpression(self, expr):
        try:
            value = self.evaluate(expr)
            print(self.stringify(value))
        except RuntimeError as error:
            # Simply re-raise the error for main.py to handle
            raise

    def interpretStatements(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as error:
            # Simply re-raise the error for main.py to handle
            raise

    def visit_literal_expr(self, expr):
        return expr.value
    
    def visit_logical_expr(self, expr):
        left = self.evaluate(expr.left)
        if expr.operator.type == TokenType.OR:
            if self.is_truthy(left):
                return left
        else:
            if not self.is_truthy(left):
                return left
        return self.evaluate(expr.right)
    
    def visit_set_expr(self, expr):
        object = self.evaluate(expr.object)
        if not isinstance(object, LoxInstance):
            raise RuntimeError(expr.name, "Only instances have fields.")
        value = self.evaluate(expr.value)
        object.set(expr.name, value)
        return value
    
    def visit_this_expr(self, expr):
        return self.lookup_variable(expr.keyword, expr)
    
    def visit_grouping_expr(self, expr):
        return self.evaluate(expr.expression)
    
    def evaluate(self, expr):
        return expr.accept(self)
    
    def execute(self, stmt):
        stmt.accept(self)

    def resolve(self, expr, depth):
        self.locals[id(expr)] = depth

    def visit_block_stmt(self, stmt):
        self.execute_block(stmt.statements, Environment(self.environment))
        return None

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous

    def visit_class_stmt(self, stmt):
        self.environment.define(stmt.name.lexeme, None)
        
        # Evaluate methods
        methods = {}
        for method in stmt.methods:
            function = LoxFunction(
                method,
                self.environment,
                method.name.lexeme == "init"
            )
            methods[method.name.lexeme] = function
            
        klass = LoxClass(stmt.name.lexeme, methods)
        self.environment.assign(stmt.name, klass)
        return None
    
    def visit_expression_stmt(self, stmt):
        self.evaluate(stmt.expression)
        return None
    
    def visit_function_stmt(self, stmt):
        function = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lexeme, function)
        return None
    
    def visit_if_stmt(self, stmt):
        if self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.then_branch)
        elif stmt.else_branch is not None:
            self.execute(stmt.else_branch)
        return None

    def visit_print_stmt(self, stmt):
        value = self.evaluate(stmt.expression)
        print(self.stringify(value))
        return None
    
    
    def visit_return_stmt(self, stmt):
        value = None
        if stmt.value is not None:
            value = self.evaluate(stmt.value)
        raise Return(value)
    
    def visit_var_stmt(self, stmt):
        value = None
        if stmt.initializer is not None:
            value = self.evaluate(stmt.initializer)
        self.environment.define(stmt.name.lexeme, value)
        return None

    def visit_while_stmt(self, stmt):
        while self.is_truthy(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None
    
    def visit_assign_expr(self, expr):
        value = self.evaluate(expr.value)
        distance = self.locals.get(id(expr))
        if distance is not None:
            self.environment.assign_at(distance, expr.name, value)
        else:
            self.globals.assign(expr.name, value)
        return value
    
    def visit_binary_expr(self, expr):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type == TokenType.PLUS:
            # Check types for addition
            if isinstance(left, float) and isinstance(right, float):
                return float(left + right)
            elif isinstance(left, str) and isinstance(right, str):
                return str(left + right)
            # If types don't match or aren't supported, raise runtime error
            raise RuntimeError(expr.operator, 
                "Operands must be two numbers or two strings.")
        
        # Handle other operators
        if expr.operator.type == TokenType.MINUS:
            self.check_number_operands(expr.operator, left, right)
            return float(left - right)
        if expr.operator.type == TokenType.GREATER:
            self.check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        if expr.operator.type == TokenType.GREATER_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        if expr.operator.type == TokenType.LESS:
            self.check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        if expr.operator.type == TokenType.LESS_EQUAL:
            self.check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(left, right)
        if expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.is_equal(left, right)
        if expr.operator.type == TokenType.COMMA:
            return left, right
        if expr.operator.type == TokenType.SLASH:
            self.check_number_operands(expr.operator, left, right)
            if float(right) == 0.0:
                raise RuntimeError(expr.operator, "Division by zero.")
            return float(left) / float(right)
        if expr.operator.type == TokenType.STAR:
            self.check_number_operands(expr.operator, left, right)
            return float(left) * float(right)
    
    def visit_call_expr(self, expr):
        callee = self.evaluate(expr.callee)
        arguments = []
        for arg in expr.arguments:
            arguments.append(self.evaluate(arg))
        if not isinstance(callee, LoxCallable):
            raise RuntimeError(expr.paren, "Can only call functions and classes.")
        function = callee
        if len(arguments) != function.arity():
            raise RuntimeError(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
        return function.call(self, arguments)
    
    def visit_get_expr(self, expr):
        object = self.evaluate(expr.object)
        if isinstance(object, LoxInstance):
            return object.get(expr.name)
        raise RuntimeError(expr.name, "Only instances have properties.")
    
    def visit_unary_expr(self, expr):
        right = self.evaluate(expr.right)
        if expr.operator.type == TokenType.BANG:
            return not self.is_truthy(right)
        elif expr.operator.type == TokenType.MINUS:
            self.check_number_operand(expr.operator, right)
            return -float(right)
        # Unreachable; return None.
        return None
    
    def visit_variable_expr(self, expr):
        return self.lookup_variable(expr.name, expr)
    
    def lookup_variable(self, name, expr):
        distance = self.locals.get(id(expr))
        if distance is not None:
            return self.environment.get_at(distance, name.lexeme)
        return self.globals.get(name)

    def check_number_operand(self, operator, operand):
        if isinstance(operand, float):
            return None
        raise RuntimeError(operator, "Operand must be a number.")

    def check_number_operands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return None
        raise RuntimeError(operator, "Operands must be numbers.")
    
    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True
    
    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
    
    def stringify(self, value):
        if value is None:
            return "nil"
        if isinstance(value, bool):
            return "true" if value else "false"
        if isinstance(value, float):
            text = str(value)
            if text.endswith(".0"):
                text = text[:-2]
            return text
        return str(value)