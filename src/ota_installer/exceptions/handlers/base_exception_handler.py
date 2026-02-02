# src/ota_installer/exceptions/handlers/base_exception_handler.py
from collections.abc import Callable
from dataclasses import dataclass, field

from ...decorators import (
    Colorizer,
    IndentWrapper,
    OutputPrinter,
)


@dataclass
class BaseExceptionHandler(object):
    """Handles exceptions for a given function with customizable messages."""

    function: Callable
    exception_type: type[BaseException] = field(default=BaseException)
    default_message: str = field(default="An error occurred")
    custom_messages: dict[type[BaseException], str] = field(
        default_factory=dict
    )

    def handle(self, *args, **kwargs) -> Callable | None:
        """Executes the function and handles exceptions."""
        try:
            return self.function(*args, **kwargs)
        except self.exception_type as err:
            self.print_exception_message(err)
            return None

    @OutputPrinter(use_color=True, prefix="\n\n", suffix="\n\n")
    def print_exception_message(self, error: BaseException) -> str:
        """Prints the formatted exception message."""
        formatted_message = self.format_message(error)
        return formatted_message

    @IndentWrapper(interval=1)
    @Colorizer(style="variable")
    def format_message(self, error: BaseException) -> str:
        """Formats the error message based on the exception type."""
        error_message = self.custom_messages.get(
            type(error), self.default_message
        )
        return f"{error_message}"

    def __call__(self, *args, **kwargs) -> Callable | None:
        """Allows the instance to be called as a function."""
        return self.handle(*args, **kwargs)


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260202
