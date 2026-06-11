# src/ota_installer/decorators/confirmation_prompt.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from functools import wraps

import pyinputplus as pyip
from rich.console import Console

from ota_installer.decorator.colorizer import Colorizer

from ..style.style_handler import RichColors

console = Console()


class PromptType(StrEnum):
    KEY_OPTION = "/".join(["Y", "N"])
    ERROR = "Invalid Option!"
    REQUEST = "Do you want to "

    @classmethod
    def get_request(cls, action: str) -> str:
        """Construct the prompt message."""
        return f"{cls.REQUEST}{action}"

    @classmethod
    def get_key_option(cls) -> str:
        """Return a string of valid key options."""
        style = RichColors["non_error".upper()]
        return f"{style.beginning()}{cls.KEY_OPTION}{style.ending()}"

    @classmethod
    def get_message(cls, indent, action) -> str:
        """Construct the prompt message."""
        return f"{indent}{cls.get_request(action)}? [{cls.get_key_option()}]: "

    @staticmethod
    def get_confirmation() -> str:
        """Get user confirmation input."""
        return pyip.inputYesNo(default="no", limit=3, blank=True) == "yes"

    @staticmethod
    def get_display(indent, action) -> None:
        """Display the confirmation prompt message."""

        def func():
            return PromptType.get_message(indent, action)

        decorated_func = Colorizer(style="task")(func)
        console.print(decorated_func(), end="")

    @staticmethod
    def on_error() -> str:
        """Return the message for invalid options."""
        from .indent_wrapper import IndentWrapper

        def func():
            return PromptType.ERROR

        decorated_func = Colorizer(style="variable")(func)
        decorated_func = IndentWrapper(interval=1)(decorated_func)

        return decorated_func()


@dataclass(frozen=True, slots=True)
class ConfirmationPrompt:
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

    def __call__(self, func: Callable) -> Callable:
        """Wrap the function with a confirmation prompt."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> Callable | None:
            prompt = PromptType
            prompt.get_display(self.begin, self.comment)
            if not self.auto_confirm and not prompt.get_confirmation():
                return None
            return func(*args, **kwargs)

        return wrapper


@ConfirmationPrompt(
    begin="Start process", comment="Are you sure", indent=2, style="info"
)
def my_function():
    """Function implementation."""
    pass
