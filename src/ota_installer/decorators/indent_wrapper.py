# /src/ota_installer/decorators/indent_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from ..styles.indentation import indentation
from .protocols.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class IndentWrapper(StringReturningDecorator):
    """Decorator that adds indentation to the output of a function."""

    interval: int = 0
    char = " "

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to add indentation to its output."""

        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{self.indent()}{result}"

        return cast(Callable[P, R], wrapper)

    def indent(self):
        """Generates the indentation string."""
        return f"{indentation(char=self.char, interval=self.interval)}"


