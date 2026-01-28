# src/ota_installer/decorators/styled_figlet_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class StyledFigletPrinter(GenericDecorator):
    """Decorator for printing styled figlet text."""

    style: str = "variable"
    font: str = "slant"
    end: str = "\n"
    use_output: bool = False

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to apply figlet and color styles."""
        from . import Colorizer, Figletizer
        from .output_printer import OutputPrinter

        decorated_function = Figletizer(font=self.font)(function)  # type: ignore[reportArgumentType]
        decorated_function = Colorizer(style=self.style)(decorated_function)

        if self.use_output:
            decorated_function = OutputPrinter(suffix=self.end)(
                decorated_function
            )

        wrapped_fn = wraps(function)(decorated_function)
        return cast(Callable[P, R], wrapped_fn)


@StyledFigletPrinter(style="variable", font="slant", use_output=True)
def welcome_message():
    """Returns a welcome message for the OTA Installer."""
    return "OTA Installer ready!"


if __name__ == "__main__":
    welcome_message()

