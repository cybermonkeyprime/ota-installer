# src/ota_installer/decorators/continue_on_keypress.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, IntEnum
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


class Specs(IntEnum):
    SPACING = 4
    INTERVAL = 20


@dataclass
class ContinueOnKeyPress(GenericDecorator):
    """Decorator that pauses execution until the user presses the Enter key."""

    indent: int = field(default=1)
    char: str = field(default=" ")

    from .colorizer import Colorizer
    from .exception_handler import ExceptionHandler
    from .multiply_string import MultiplyString
    from .output_printer import OutputPrinter

    def __post_init__(self) -> None:
        self.specs = Enum(
            "Specs",
            {
                "CHAR": self.char[0],
                "SPACING": Specs.SPACING,
                "INTERVAL": Specs.INTERVAL,
            },
        )

    @ExceptionHandler()
    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to display a message and wait for user input."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            self.display_message()
            input()
            return result

        return cast(Callable[P, R], wrapper)

    def create_indentation(self) -> str:
        """
        Creates an indentation string based on the specified character and
        indent level.
        """
        return self.string()

    @MultiplyString(interval=(Specs.SPACING.value * Specs.INTERVAL.value))
    def string(self) -> str:
        """Generates a string for display based on the specified character."""
        return f"{self.char[0]}"

    @OutputPrinter(prefix="\n", suffix="")
    @Colorizer(style="title")
    def display_message(self) -> str:
        """Displays a message prompting the user to continue."""
        message = "Press the Enter key to continue... "
        return message


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260202
