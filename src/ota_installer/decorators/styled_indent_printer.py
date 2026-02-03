# src/ota_installer/decorators/styled_indent_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class StylizedIndentPrinter(GenericDecorator):
    """
    Decorator that applies stylized indentation and colorization to a
    function's output.
    """

    style: str = "variable"
    indent: int = 0
    begin: str = ""
    end: str = ""
    use_output: bool = False

    def __call__(self, function: Callable) -> Callable:
        """
        Wraps the given function with stylized indentation and colorization.
        """
        from . import Colorizer, IndentWrapper
        from .output_printer import OutputPrinter

        decorated_function = IndentWrapper(interval=self.indent)(function)
        decorated_function = Colorizer(style=self.style)(decorated_function)

        if self.use_output:
            decorated_function = OutputPrinter(suffix=self.end)(
                decorated_function
            )

        wrapped_fn = wraps(function)(decorated_function)
        return wrapped_fn


# Signed off by Brian Sanford on 20260203
