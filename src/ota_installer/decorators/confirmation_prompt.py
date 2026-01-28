# src/ota_installer/decorators/confirmation_prompt.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

import pyinputplus as pyip
from loguru import logger
from rich.console import Console

from ..styles.palette import RichColors
from .protocols.decorator_protocols import GenericDecorator

console = Console()


@dataclass
class ConfirmationPrompt(GenericDecorator):
    """
    Decorator to prompt for user confirmation before executing a function.
    """

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
        """Wrap the function with a confirmation prompt."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R | None:
            try:
                console.print(self.display_prompt(), end="")
                if not self.auto_confirm:
                    confirm = pyip.inputYesNo(
                        default="no",
                        limit=3,
                        blank=True,
                    )
                    if confirm != "yes":
                        return None
                return function(*args, **kwargs)
            except Exception as err:
                logger.exception(
                    f"{function.__name__} raised an exception: {err}"
                )
                return None

        return cast(Callable[P, R], wrapper)

    # @Printer(prefix="", suffix="")
    @Colorizer(style="task")
    def display_prompt(self) -> str:
        """Display the confirmation prompt message."""

        return f"{self.begin}{self.prompt_message()}? [{self.ending()}]: "

    def prompt_message(self) -> str:
        """Construct the prompt message."""

        return f"Do you want to {self.comment}"

    def get_confirmation(self) -> bool:
        """Get user confirmation input."""

        return pyip.inputYesNo(default="no", limit=3, blank=True) == "yes"

    def valid_options(self) -> list[str]:
        """Return valid options for confirmation."""

        return ["Y", "N"]

    def key_options(self) -> str:
        """Return a string of valid key options."""

        return "/".join(self.valid_options())

    @Colorizer(style="variable")
    @IndentWrapper(interval=1)
    def invalid_option_message(self) -> str:
        """Return the message for invalid options."""

        return "Invalid Option!"

    @IndentWrapper(interval=1)
    def beginning(self) -> str:
        """Return the beginning part of the prompt."""

        return self.begin

    def ending(self) -> str:
        """Return the ending part of the prompt with styled options."""

        style = RichColors["non_error".upper()]
        return f"{style.beginning()}{self.key_options()}{style.ending()}"


@ConfirmationPrompt(
    begin="Start process", comment="Are you sure", indent=2, style="info"
)
def my_function():
    """Function implementation."""
    pass


