from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Optional, TypeVar

from build.decorators import Colorizer, Indent, Printer
from build.styles import Colors

# Define a generic type for the decorator
F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class ConfirmationPrompt:
    begin: str = field(default="")
    comment: str = field(default="")
    indent: int = field(default=0)
    char: str = field(default="")
    debug: bool = field(default=False)
    style: str = field(default="")

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
                print(f"{function.__name__} raised an exception: {err}")
                return None

        return wrapper  # type: ignore

    @Printer(prefix="", suffix="")
    @Colorizer(style="info")
    def display_prompt(self) -> str:
        message = "Do you want to "
        prompt_message = f"{self.begin}{message}{self.comment}? {
            self.ending()}]: "
        return prompt_message

    def valid_options(self) -> list[str]:
        return ["Y", "N"]

    def key_options(self) -> str:
        return "/".join(self.valid_options())

    @Colorizer(style="warning")
    @Indent(interval=1)
    def invalid_option_message(self) -> str:
        return "Invalid Option!"

    @Indent(interval=1)
    def beginning(self) -> str:
        return f"{self.begin}"

    def message_formatter(self):
        return f"{self.comment}"

    def ending(self) -> str:
        return f"{Colors.default}[{self.key_options()}"


# Example usage:
# @ConfirmationPrompt(begin="Start process", comment="Are you sure", indent=2, style="info")
# def my_function():
#     # Function implementation
#     pass
