# src/ota_installer/exceptions/handlers/base_exception_handler.py
from collections.abc import Callable
from dataclasses import dataclass, field

from .. import decorator


@dataclass(slots=True)
class BaseExceptionHandler:
    """Handles exceptions for a given function with customizable messages."""

    function: Callable
    exception_type: type[BaseException] = field(default=BaseException)
    default_message: str = field(default="An error occurred")
    custom_messages: dict[type[BaseException], str] = field(
        default_factory=dict
    )

    def handle(self, *args, **kwargs) -> Callable | None:
        """Executes the function and handles exceptions."""
        if callable(self.function):
            return self.function(*args, **kwargs)
        return None

    @decorator.OutputPrinter(use_color=True, prefix="\n\n", suffix="\n\n")
    def print_exception_message(self, error: BaseException) -> str:
        """Prints the formatted exception message."""
        return self.format_message(error)

    @decorator.IndentWrapper(interval=1)
    @decorator.Colorizer(style="variable")
    def format_message(self, error: BaseException) -> str:
        """Formats the error message based on the exception type."""
        return self.custom_messages.get(type(error), self.default_message)

    def __call__(self, *args, **kwargs) -> Callable | None:
        """Allows the instance to be called as a function."""
        return self.handle(*args, **kwargs)


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260626
