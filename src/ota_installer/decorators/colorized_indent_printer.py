# src/ota_installer/decorators/colorized_indent_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class ColorizedIndentPrinter(StringReturningDecorator):
    """
    Decorator that applies colorization and indentation to the output of a
    function.
    """

    indent: int = 0
    begin: str = ""
    end: str = ""
    style: str = "variable"

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the given function to apply colorization and indentation."""
        from . import Colorizer, IndentWrapper, OutputPrinter

        @OutputPrinter(use_color=False)
        @Colorizer(style=self.style)
        @IndentWrapper(interval=self.indent)
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{result}"

        return cast(Callable[P, R], wrapper)


# Signed off by Brian Sanford on 20260120
