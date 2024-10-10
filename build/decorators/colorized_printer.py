from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from .colorizer import Colorizer
from .printer import Printer


@dataclass
class ColorizedPrinter:
    begin: str = ""
    end: str = ""
    style: str = "variable"

    def __call__(self, function: Callable) -> Any:
        @Printer(color=False)
        @Colorizer(style=self.style)
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return f"{result}"

        return inner
