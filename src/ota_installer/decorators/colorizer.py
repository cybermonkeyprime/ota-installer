# src/ota_installer/decorators/colorizer.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps

from ..styles.palette import RichColors
from .protocols.decorator_protocols import StringReturningDecorator

type R = str


@dataclass
class Colorizer(StringReturningDecorator):
    """
    Colorizer decorator — applies ANSI style to the result of string-returning
    functions.
    """

    style: str = field(default="")

    def __post_init__(self) -> None:
        """Initializes the color attribute based on the provided style."""
        self.color = RichColors[self.style.upper()]
        if self.color is None:
            raise ValueError(f"Invalid style: {self.style}")

    def __call__(self, function: Callable) -> Callable:
        """Wraps the function to apply color styling to its return value."""

        @wraps(function)
        def wrapper(*args, **kwargs) -> R:
            """
            Wrapper function that executes the original function and styles
            its output.
            """
            result = function(*args, **kwargs)
            return f"{self.color.beginning()}{result}{self.color.ending()}"

        return wrapper


def main() -> None:
    # Example usage
    colorizer = Colorizer(style="task")

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260209
