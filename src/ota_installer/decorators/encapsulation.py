# src/ota_installer/decorators/encapsulation.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import wraps

from .protocols.decorator_protocols import GenericDecorator


class SeparatorSpecs(Enum):
    CHAR = "="
    SPACING = 4
    INTERVAL = 20


@dataclass
class Encapsulate(GenericDecorator):
    """Decorator class to encapsulate function calls with separators."""

    from .multiply_string import MultiplyString
    from .output_printer import OutputPrinter

    def __call__(self, function: Callable) -> Callable:
        """
        Wraps the function with separator calls before and after execution.
        """

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            self._print_separator()
            result = function(*args, **kwargs)
            self._print_separator()
            return result

        return wrapper

    @OutputPrinter(prefix="\n", suffix="\n\n")
    @MultiplyString(
        interval=(SeparatorSpecs.SPACING.value * SeparatorSpecs.INTERVAL.value)
    )
    def _print_separator(self) -> str:
        """Prints a separator line."""
        return SeparatorSpecs.CHAR.value


# Signed off by Brian Sanford on 20260203
