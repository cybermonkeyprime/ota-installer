from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any
from build.decorators.colorizer import Colorizer
from build.decorators.figletizer import Figletizer

"""
Do not use this causes circlular import
circular until resolved
from build.decorators import Colorizer, Figletizer
"""


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
