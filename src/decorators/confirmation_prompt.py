# src/decorators/confirmation_prompt.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

import pyinputplus as pyip

from src.styles.palette import Colors
from src.types.decorators import GenericDecorator


@dataclass
class ConfirmationPrompt(GenericDecorator):
    begin: str = field(default="")
    comment: str = field(default="")
    indent: int = field(default=0)
    char: str = field(default="")
    debug: bool = field(default=False)
    style: str = field(default="")
    auto_confirm: bool = False

    from . import Colorizer
    from .indent_wrapper import IndentWrapper

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            try:
                self.display_prompt()
                if not self.auto_confirm:
                    confirm = pyip.inputYesNo(
                        prompt=self.display_prompt(),
                        default="no",
                        limit=3,
                        blank=True,
                    )
                    if confirm != "yes":
                        return None
                return function(*args, **kwargs)
            except Exception as err:
                print(f"{function.__name__} raised an exception: {err}")
                return None

        return cast(Callable[P, R], wrapper)

    # @Printer(prefix="", suffix="")
    @Colorizer(style="task")
    def display_prompt(self) -> str:
        message = "Do you want to "
        prompt_message = (
            f"{self.begin}{message}{self.comment}? {self.ending()}]: "
        )
        return prompt_message

    def valid_options(self) -> list[str]:
        return ["Y", "N"]

    def key_options(self) -> str:
        return "/".join(self.valid_options())

    @Colorizer(style="variable")
    @IndentWrapper(interval=1)
    def invalid_option_message(self) -> str:
        return "Invalid Option!"

    @IndentWrapper(interval=1)
    def beginning(self) -> str:
        return f"{self.begin}"

    def message_formatter(self):
        return f"{self.comment}"

    def ending(self) -> str:
        return f"{Colors.reset}[{self.key_options()}{Colors.reset}"


""" Example usage:"""


@ConfirmationPrompt(
    begin="Start process", comment="Are you sure", indent=2, style="info"
)
def my_function():
    # Function implementation
    pass
