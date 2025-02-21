from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.styles import Indentation


@dataclass
class IndentString:
    interval: int = 0

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return f"{self.indentation()}{result}"

        return wrapper

    def indentation(self) -> str:
        return f"{Indentation(interval=self.interval)}"
