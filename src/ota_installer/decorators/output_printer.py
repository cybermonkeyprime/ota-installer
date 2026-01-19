# src/ota_installer/decorators/output_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from rich.console import Console

from .protocols.decorator_protocols import GenericDecorator

console = Console()


@dataclass
class OutputPrinter(GenericDecorator):
    """Decorator for printing function output with optional styling."""

    prefix: str = ""
    use_color: bool = False
    suffix: str = "\n"
    color: str = "non_error"

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to print its output with specified formatting."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            from ..styles import RichColors

            style = RichColors[self.color.upper()]

            try:
                result = function(*args, **kwargs)
                console.print(
                    f"{style.beginning()}{self.prefix}{result}{style.ending()}",
                    highlight=False,
                    end=self.suffix,
                )
                return result
            except Exception as e:
                raise RuntimeError(
                    f"{function.__name__}(): "
                    "An error occurred while executing the function: {e}"
                ) from e

        return cast(Callable[P, R], wrapper)


# Signed off by Brian Sanford on 20260118
