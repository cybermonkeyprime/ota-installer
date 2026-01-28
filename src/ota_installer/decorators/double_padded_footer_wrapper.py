# src/ota_installer/decorators/double_padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

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

    from . import Colorizer
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to add a double padded footer."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            self._output_footer(self.beginning)
            logger.debug(self.message)
            self._output_footer(self.message)
            self._output_footer(self.ending)
            return result

        return cast(Callable[P, R], wrapper)

    @OutputPrinter(use_color=False)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)
    def _output_footer(self, message: str) -> str:
        """Outputs the footer messages."""
        return f"{message}"


if __name__ == "__main__":
    pass
