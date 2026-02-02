# src/ota_installer/decorators/figletizer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps

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

    def __call__(self, function: Callable) -> Callable:
        """Wraps the given function to format its output with figlet."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> R:
            """
            Wrapper function that calls the original function and formats its
            output.
            """
            result = function(*args, **kwargs)
            return f"{figlet_format(str(result), font=self.font)}"

        return wrapper


# Signed off by Brian Sanford on 20260202
