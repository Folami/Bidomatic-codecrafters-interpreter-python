# Assuming LoxClass is defined, possibly in another file.
# We use a forward reference string 'LoxClass' for the type hint,
# or import it conditionally.
from typing import Dict, Any, TYPE_CHECKING

# Import supporting classes if needed for full functionality (e.g., get/set)
# from app.token import Token
# from app.runtime_error import RuntimeError
# from app.lox_function import LoxFunction # If methods are involved

if TYPE_CHECKING:
    # This helps type checkers find LoxClass without causing circular imports at runtime
    from app.lox_class import LoxClass # Adjust path as needed

from .lox_function import LoxFunction
from .runtime_error import RuntimeError

class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields = {}

    def get(self, name):
        if name.lexeme in self.fields:
            return self.fields[name.lexeme]

        method = self.klass.find_method(name.lexeme)
        if method:
            return method.bind(self)

        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name, value):
        self.fields[name.lexeme] = value

    def __str__(self):
        return f"{self.klass.name} instance"

# Example Usage (requires LoxClass, Token, RuntimeError definitions):
# class LoxClass: # Dummy for example
#     def __init__(self, name): self.name = name
#     def find_method(self, name): return None # Dummy method lookup
#
# class Token: # Dummy for example
#     def __init__(self, lexeme): self.lexeme = lexeme; self.line = 1
#
# class RuntimeError(Exception): # Dummy for example
#     def __init__(self, token, message): super().__init__(message); self.token = token
#
# if __name__ == '__main__':
#     my_klass = LoxClass("MyWidget")
#     my_instance = LoxInstance(my_klass)
#     print(my_instance) # Output: MyWidget instance
#
#     # Example setting/getting fields (requires Token)
#     name_token = Token("color")
#     my_instance.set(name_token, "red")
#     print(my_instance.get(name_token)) # Output: red
