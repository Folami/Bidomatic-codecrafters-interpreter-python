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


class LoxInstance:
    """Represents an instance of a Lox class."""

    def __init__(self, klass: 'LoxClass'):
        """
        Initializes a LoxInstance.
        Args:
            klass: The LoxClass of which this is an instance.
        """
        # Python doesn't have strict private. Convention uses a leading underscore
        # to indicate an attribute is intended for internal use.
        self._klass: 'LoxClass' = klass
        # Instances need fields to store their state. This corresponds to the
        # HashMap often used in the Java version.
        self._fields: Dict[str, Any] = {}

    def get(self, name: 'Token'): # Assuming Token is used for field names
        """Gets a field or method from the instance."""
        # Check instance fields first
        if name.lexeme in self._fields:
            return self._fields[name.lexeme]

        # If field not found, look for a method on the class
        # This requires LoxClass to have a find_method implementation
        method = self._klass.find_method(name.lexeme)
        if method is not None:
            # Bind 'this' (self in Python) to the instance when returning the method
            # This requires LoxFunction to have a bind method
            return method.bind(self)

        # If neither field nor method is found
        # Assuming RuntimeError and Token classes are available
        raise RuntimeError(name, f"Undefined property '{name.lexeme}'.")

    def set(self, name: 'Token', value: Any):
         """Sets a field on the instance."""
         # Simply store the value in the instance's field dictionary
         self._fields[name.lexeme] = value

    def __str__(self) -> str:
        """
        Returns the string representation of the instance.
        Equivalent to Java's toString().
        """
        # Access the class name via the internal attribute
        return self._klass.name + " instance"

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
