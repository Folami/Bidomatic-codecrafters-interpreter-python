from abc import ABC, abstractmethod
from typing import Any, List

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        """Return the number of arguments this callable accepts."""
        pass
    
    @abstractmethod
    def call(self, interpreter: Any, arguments: List[Any]) -> Any:
        pass