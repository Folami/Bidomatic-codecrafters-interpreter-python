from abc import ABC, abstractmethod
from typing import Any, List
# from app.interpreter import Interpreter

class LoxCallable(ABC):
    @abstractmethod
    def arity(self) -> int:
        """Return the number of arguments this callable accepts."""
        from app.interpreter import Interpreter
        pass

    @abstractmethod
    def call(self, interpreter: Interpreter, arguments: List[Any]) -> Any:
        from app.interpreter import Interpreter
        pass