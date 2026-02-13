# src/ota_installer/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from ..containers.decorators import Decorators
from ..log_setup import logger
from .protocols.decorator_protocols import GenericDecorator


@dataclass
class DoublePaddedFooterWrapper(GenericDecorator):
    """
    Decorator that adds a double padded footer to the output of a function.
    """

    beginning: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to add a double padded footer."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> object:
            result = function(*args, **kwargs)
            self._print_footer(self.beginning)
            logger.debug(self.message)
            self._print_footer(self.message)
            self._print_footer(self.ending)
            return result

        return wrapper

    @Decorators.output_printer(use_color=False)
    @Decorators.colorizer(style="variable")
    @Decorators.indent_wrapper(interval=1)
    def _print_footer(self, message: str) -> str:
        """Outputs the footer messages."""
        return f"{message}"


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260213
