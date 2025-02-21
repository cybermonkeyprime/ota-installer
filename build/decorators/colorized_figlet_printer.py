from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.decorators.colorizer import Colorizer
from build.decorators.figletizer import Figletizer
from build.decorators.printer import Printer

"""
Do not use this causes circlular import
circular until resolved
from build.decorators import Colorizer, Figletizer, Printer
"""


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
