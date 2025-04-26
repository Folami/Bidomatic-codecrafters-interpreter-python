from abc import ABC, abstractmethod
from typing import Any, List, TYPE_CHECKING # Import TYPE_CHECKING

# Conditionally import Interpreter only when type checking is performed
# This breaks the runtime circular dependency.
if TYPE_CHECKING:
    from app.interpreter import Interpreter

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        """Return the number of arguments this callable accepts."""
        # Remove the import from here if it exists
        pass

    @abstractmethod
    def call(self, interpreter: 'Interpreter', arguments: List[Any]) -> Any:
        """Execute the callable's logic."""
        # Use 'Interpreter' as a string literal (forward reference)
        # Remove the import from here if it exists
        pass

    # Add __str__ if needed, but it doesn't cause the import issue
    # @abstractmethod
    # def __str__(self) -> str:
    #     pass
