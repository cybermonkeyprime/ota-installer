# src/ota_installer/decorators/padded_footer_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class PaddedFooterWrapper(GenericDecorator):
    """Decorator that adds a padded footer to the output of a function."""

    padding: str = field(default="")

    from . import Colorizer
    from .indent_wrapper import IndentWrapper
    from .output_printer import OutputPrinter

    def __call__(self, function: Callable) -> Callable:
        """Wraps the given function to add a padded footer."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> Callable:
            result = function(*args, **kwargs)
            self._add_padding()
            return result

        return wrapper

    @OutputPrinter(use_color=True)
    @Colorizer(style="variable")
    @IndentWrapper(interval=1)  # type: ignore[return-value]
    def _add_padding(self) -> object:
        return f"{self.padding}"


# Signed off by Brian Sanford on 20260209
