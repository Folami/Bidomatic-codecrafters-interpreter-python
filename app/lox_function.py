from app.lox_callable import LoxCallable
from app.environment import Environment
from app.stmt import Function
from app.return_exception import Return


class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function, closure: Environment=None, is_initializer: bool=False):
        self.is_initializer = is_initializer
        self.declaration = declaration
        self.closure = closure

    def bind(self, instance):
        # Bind the instance to the function, creating a new environment.
        environment = Environment(self.closure)
        environment.define("this", instance)
        # Return a new LoxFunction with the bound environment.
        return LoxFunction(self.declaration, environment, self.is_initializer)

    def arity(self) -> int:
        # Return the number of parameters in the function declaration.
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        # Create new environment for function execution
        environment = Environment(self.closure)
        
        # Bind parameters to arguments
        for i in range(len(self.declaration.params)):
            environment.define(
                self.declaration.params[i].lexeme, 
                arguments[i]
            )
        
        try:
            # Execute function body
            interpreter.execute_block(self.declaration.body, environment)
        except Return as return_value:
            if self.is_initializer:
                return self.closure.get_at(0, "this")
            return return_value.value
            
        if self.is_initializer:
            return self.closure.get_at(0, "this")
        return None

    def __str__(self) -> str:
        return "<fn " + self.declaration.name.lexeme + ">"
