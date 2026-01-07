# src/ota_installer/decorators/colorizer.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

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
        self.color = RichColors[self.style.upper()]

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = function(*args, **kwargs)
                styled_result = (
                    f"{self.color.beginnning()}{result}{self.color.ending()}"
                )
            except AttributeError as error:
                raise ValueError("Invalid style attribute: ") from error
            return styled_result

        return cast(Callable[P, R], wrapper)


if __name__ == "__main__":
    # Example usage
    colorizer = Colorizer(style="task")

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))
