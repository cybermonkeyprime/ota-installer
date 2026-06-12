# src/ota_installer/decorators/continue_on_keypress.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
from functools import wraps

from ..style.style_handler import StyleRenderer


class Specs(IntEnum):
    SPACING = 4
    INTERVAL = 20


class Message(StrEnum):
    PROMPT = "Press the Enter key to continue... "


@dataclass
class ContinueOnKeyPress:
    """Decorator that pauses execution until the user presses the Enter key."""

    indent: int = field(default=1)
    char: str = field(default=" ")

    from .colorizer import Colorizer
    from .exception_handler import ExceptionHandler
    from .multiply_string import MultiplyString
    from .output_printer import OutputPrinter

    @ExceptionHandler()
    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to display a message and wait for user input."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            result = function(*args, **kwargs)
            self.display_message()
            input()
            return result

        return wrapper

    def create_indentation(self) -> str:
        """
        Creates an indentation string based on the specified character and
        indent level.
        """
        render_style = StyleRenderer(
            self.char[0], Specs.SPACING, Specs.INTERVAL
        )
        return render_style()

    def display_message(self) -> str:
        """Displays a message prompting the user to continue."""
        from .colorizer import Colorizer
        from .output_printer import OutputPrinter

        def func():
            return Message.PROMPT

        decorated_func = OutputPrinter(prefix="\n", suffix="")(func)
        decorated_func = Colorizer(style="title")(decorated_func)
        return decorated_func()


if __name__ == "__main__":
    pass
