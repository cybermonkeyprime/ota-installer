from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


@dataclass
class StyleWrapper:
    style: str = ""
    newline: bool = False

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            print(f"{self.style}{result}", end=self.new_line())
            return result

        return wrapper

    def new_line(self) -> str:
        return "\n" if self.newline else ""
