from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable

from .multiply_string import MultiplyString
from .printer import Printer


@dataclass
class Encapsulate:
    interval: int = field(default=0)

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.start()
            result = function(*args, **kwargs)
            self.end()
            return result

        return wrapper

    @MultiplyString(interval=4)
    @MultiplyString(interval=20)
    def separator(self) -> str:
        return "="

    @Printer(prefix="\n", suffix="\n\n")
    def start(self):
        return self.separator()

    @Printer(prefix="\n", suffix="\n\n")
    def end(self):
        return self.separator()
