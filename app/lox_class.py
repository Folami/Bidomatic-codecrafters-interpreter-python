# No direct equivalent imports needed for this specific class structure,
# but 'typing' is good practice for type hints.
from typing import Any # Optional: Use Any if methods might be added later
from app.lox_callable import LoxCallable
from app.lox_instance import LoxInstance

class LoxClass(LoxCallable):
    """Represents a Lox class definition at runtime."""

    def __init__(self, name: str, superclass: 'LoxClass' = None, methods: dict = None):
        """
        Initializes a LoxClass.
        Args:
            name: The name of the class.
        """
        self.superclass = superclass
        self.name: str = name
        self.methods: dict = methods if methods is not None else {}

    def __str__(self) -> str:
        """
        Returns the string representation of the class (its name).
        Equivalent to Java's toString().
        """
        return self.name
    
    def arity(self) -> int:
        """
        Returns the number of parameters for the class constructor.
        In Lox, this is always 0 since classes don't have a constructor.
        """
        initializer = self.find_method("init")
        if initializer:
            return initializer.arity()
        return 0

    def find_method(self, name):
        """
        Finds a method by name in the class.
        Args:
            name: The name of the method to find.
        Returns:
            The method if found, otherwise None.
        """
        if name in self.methods:
            return self.methods[name]
        if self.superclass:
            return self.superclass.find_method(name)
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
        
        # Look for initializer
        initializer = self.find_method("init")
        if initializer:
            initializer.bind(instance).call(interpreter, arguments)
            
        return instance
