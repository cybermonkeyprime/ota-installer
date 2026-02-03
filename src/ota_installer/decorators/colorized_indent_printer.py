# src/ota_installer/decorators/colorized_indent_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from ..containers.decorators import Decorators
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

    def __call__(self, function: Callable) -> Callable:
        """Wraps the given function to apply colorization and indentation."""

        @Decorators.output_printer(use_color=False)
        @Decorators.colorizer(style=self.style)
        @Decorators.indent_wrapper(interval=self.indent)
        @wraps(function)
        def wrapper(*args, **kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{result}"

        return wrapper


# Signed off by Brian Sanford on 20260203
