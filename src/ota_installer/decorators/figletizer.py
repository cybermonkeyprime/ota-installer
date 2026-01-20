# src/ota_installer/decorators/figletizer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from pyfiglet import figlet_format

from .protocols.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class Figletizer(StringReturningDecorator):
    """
    Decorator that formats the output of a function using a specified figlet
    font.
    """

    font: str = "slant"

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the given function to format its output with figlet.

        Args:
            function: The function to be wrapped.

        Returns:
            A wrapper function that applies figlet formatting to the output.
        """

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            Wrapper function that calls the original function and formats its
            output.
            """
            result = function(*args, **kwargs)
            return f"{figlet_format(str(result), font=self.font)}"

        return cast(Callable[P, R], wrapper)


# Signed off by Brian Sanford on 20260119
