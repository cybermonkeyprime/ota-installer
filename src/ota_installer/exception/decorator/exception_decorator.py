# src/ota_installer/exception/decorator/exception_decorator.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from ...style import decorator as style
from ...style.style_renderer import indentation
from .protocol.decorator_protocols import GenericDecorator


@dataclass(frozen=True, slots=True)
class ExceptionDecorator(GenericDecorator):
    """Handle a specific exception and display a styled message."""

    style: str
    exception_type: type[BaseException]

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapper(*args, **kwargs) -> object | None:
            try:
                return function(*args, **kwargs)
            except self.exception_type:
                self.display_message()
                return None

        return wrapper

    def display_message(self) -> None:
        line_break = "\n\n"
        exception = f"{self.exception_type.__name__}"

        def message() -> str:
            return (
                f"{line_break}"
                f"{indentation()}{exception} detected, aborting safely"
                f"{line_break}"
            )

        decorated = style.StylizedIndentPrinter(
            style=self.style,
            indent=1,
            use_output=True,
        )(message)

        decorated()


# Signed off by Brian Sanford on 20260912
