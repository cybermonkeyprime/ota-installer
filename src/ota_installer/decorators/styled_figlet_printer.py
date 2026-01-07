# src/ota_installer/decorators/styled_figlet_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class StyledFigletPrinter(GenericDecorator):
    style: str = "variable"
    font: str = "slant"
    end: str = "\n"
    use_output: bool = False

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        from . import Colorizer, Figletizer
        from .output_printer import OutputPrinter

        decorated = Figletizer(font=self.font)(function)  # type: ignore[reportArgumentType]
        decorated = Colorizer(style=self.style)(decorated)

        if self.use_output:
            decorated = OutputPrinter(suffix=self.end)(decorated)

        wrapped_fn = wraps(function)(decorated)
        return cast(Callable[P, R], wrapped_fn)


@StyledFigletPrinter(style="variable", font="slant", use_output=True)
def welcome_message():
    return "OTA Installer ready!"


if __name__ == "__main__":
    welcome_message()
