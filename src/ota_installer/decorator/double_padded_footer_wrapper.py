# src/ota_installer/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from functools import wraps

from ..log_setup import logger
from .container.decorator_container import Decorators
from .protocol.decorator_protocols import GenericDecorator


class DecoratorType(StrEnum):
    MESSAGE = "Finished!"
    STYLE = "variable"


@dataclass
class DoublePaddedFooterWrapper(GenericDecorator):
    """
    Decorator that adds a double padded footer to the output of a function.
    """

    beginning: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    def __call__(self, func: Callable) -> Callable:
        """Wraps the function to add a double padded footer."""
        style = DecoratorType

        @wraps(func)
        def wrapper(*args, **kwargs) -> object:
            result = func(*args, **kwargs)
            logger.debug(style.MESSAGE)
            self._print_footer(style.MESSAGE)
            return result

        return wrapper

    def _print_footer(self, text: str) -> str:
        """Outputs the footer messages."""

        def func():
            return text

        decorated_func = Decorators.output_printer(use_color=False)(func)
        decorated_func = Decorators.colorizer(style="variable")(decorated_func)
        decorated_func = Decorators.indent_wrapper(interval=1)(decorated_func)
        return decorated_func()


if __name__ == "__main__":
    pass
