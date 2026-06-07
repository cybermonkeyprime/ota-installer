# src/ota_installer/decorators/figletizer.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import StrEnum, auto
from functools import wraps

from pyfiglet import figlet_format

from .protocol.decorator_protocols import StringReturningDecorator


class FontType(StrEnum):
    SLANT = auto()


@dataclass
class Figletizer(StringReturningDecorator):
    """
    Decorator that formats the output of a function using a specified figlet
    font.
    """

    font: str = "slant"

    def __call__(self, func: Callable) -> Callable:
        """Wraps the given function to format its output with figlet."""

        @wraps(func)
        def wrapper(*args, **kwargs) -> str:
            """
            Wrapper function that calls the original function and formats its
            output.
            """
            result = func(*args, **kwargs)
            return f"{figlet_format(str(result), font=FontType.SLANT)}"

        return wrapper
