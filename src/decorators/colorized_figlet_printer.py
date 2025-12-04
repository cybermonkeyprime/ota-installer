# src/decorators/colorized_figlet_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast


@dataclass
class ColorizedFigletOutputPrinter(object):
    color: bool = True
    end: str = "\n"
    style: str = "variable"
    font: str = "slant"

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        from . import Colorizer, Figletizer
        from .output_printer import OutputPrinter

        @OutputPrinter(suffix=self.end)
        @Colorizer(style=self.style)
        @Figletizer(font=self.font)  # type: ignore[return-value]
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return result

        return cast(Callable[P, R], wrapper)
