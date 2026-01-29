# /src/ota_installer/decorators/indent_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass

from ..styles.indentation import indentation
from .protocols.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class IndentWrapper(StringReturningDecorator):
    """Decorator that adds indentation to the output of a function."""

    interval: int = 0
    char = " "

    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to add indentation to its output."""

        def wrapper(*args, **kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{self.indent()}{result}"

        return wrapper

    def indent(self):
        """Generates the indentation string."""
        return f"{indentation(char=self.char, interval=self.interval)}"


# Signed off by Brian Sanford on 20260129
