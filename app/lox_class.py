# No direct equivalent imports needed for this specific class structure,
# but 'typing' is good practice for type hints.
from typing import Any # Optional: Use Any if methods might be added later
from app.lox_callable import LoxCallable
from app.lox_instance import LoxInstance

class LoxClass(LoxCallable):
    """Represents a Lox class definition at runtime."""

    def __init__(self, name: str, methods: dict):
        """
        Initializes a LoxClass.
        Args:
            name: The name of the class.
        """
        self.name: str = name
        self.methods: dict = methods  # Store methods dictionary

    def __str__(self) -> str:
        """
        Returns the string representation of the class (its name).
        Equivalent to Java's toString().
        """
        return self.name

    def get_method(self, name):
        """
        Finds a method by name in the class.
        Args:
            name: The name of the method to find.
        Returns:
            The method if found, None otherwise.
        """
        if name.lexeme in self.methods:
            return self.methods[name.lexeme]
        return None
    
    def call(self, interpreter, arguments):
        """
        Calls the class to create an instance.
        Args:
            interpreter: The interpreter instance.
            arguments: The arguments for the call.
        Returns:
            The created instance.
        """
        instance = LoxInstance(self)
        return instance
    
    def arity(self) -> int:
        """
        Returns the number of parameters in the class constructor.
        """
        initializer = self.find_method("init")
        if initializer is None:
            return 0
        return initializer.arity()
