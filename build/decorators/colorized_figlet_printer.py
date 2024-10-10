from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from .colorizer import Colorizer
from .figletizer import Figletizer
from .printer import Printer


@dataclass
class ColorizedFigletPrinter:
    color: bool = True
    end: str = "\n"
    style: str = "variable"
    font: str = "slant"

    def __call__(self, function: Callable) -> Any:
        @Printer(suffix=self.end)
        @Colorizer(style=self.style)
        @Figletizer(font=self.font)
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return result

        return inner
