from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Optional, TypeVar

from build.decorators import Colorizer, Indent, Printer
from build.styles import Colors, indentation

# Define a generic type for the decorator
F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class ConfirmationPrompt:
    """
    A class that provides a confirmation prompt before executing a function.

    Attributes:
        introduction: A string to introduce the prompt.
        question: A string representing the question to ask the user.
        indentation_level: An integer representing the indentation level
        for the prompt.
        confirmation_char: A string representing the character
        for confirmation.
        debug_mode: A boolean indicating if debug mode is enabled.
    """

    begin: str = field(default="")
    question: str = field(default="")
    indentation_level: int = field(default=0)
    confirmation_char: str = field(default="")
    debug_mode: bool = field(default=False)

    def __call__(self, function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Optional[Any]:
            self.display_prompt()
            key = input().strip().upper()
            try:
                if key in self.valid_options():
                    if key == "Y":
                        return function(*args, **kwargs)
                else:
                    print(self.invalid_option_message())
                    return wrapper(*args, **kwargs)
            except Exception as err:
                if self.debug_mode:
                    print(f"{function.__name__} raised an exception: {err}")
                return None

        #            return wrapper(*args, **kwargs)

        return wrapper  # type: ignore

    @Printer(prefix="", suffix="")
    @Colorizer(style="info")
    def display_prompt(self) -> str:
        prompt_message = f"{self.begin}{self.question} {self.ending()}]: "
        return prompt_message

    def valid_options(self) -> "list[str]":
        return ["Y", "N"]

    def key_options(self) -> str:
        return "/".join(self.valid_options())

    @Colorizer(style="warning")
    @Indent(interval=1)
    def invalid_option_message(self) -> str:
        return "Invalid Option!"

    @Indent(interval=indentation_level)
    def beginning(self) -> str:
        return f"{self.begin}"

    def message_formatter(self):
        return f"{self.question}"

    def ending(self) -> str:
        return f"{Colors.default}[{self.key_options()}"


# Example usage:
# @ConfirmationPrompt(begin="Start process", comment="Are you sure", indent=2, style="info")
# def my_function():
#     # Function implementation
#     pass
