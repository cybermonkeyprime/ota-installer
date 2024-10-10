from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from .colorizer import Colorizer
from .figletizer import Figletizer


@dataclass
class ColorizedFiglet:
    style: str = "variable"
    font: str = "slant"

    def __call__(self, function: Callable) -> Any:
        @Colorizer(style=self.style)
        @Figletizer(font=self.font)
        @wraps(function)
        def inner(*args, **kwargs) -> Any:
            result = function(*args, **kwargs)
            return result

        return inner
