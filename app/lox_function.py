from app.lox_callable import LoxCallable
from app.environment import Environment
from app.stmt import Function
from app.return_ import Return

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment=None) -> None:
        self.declaration = declaration
        self.closure = closure

    def arity(self) -> int:
        # Return the number of parameters in the function declaration.
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for i, param in enumerate(self.declaration.params):
            environment.define(param.lexeme, arguments[i])
        try:
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            return return_value.value
        return None

    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"
    