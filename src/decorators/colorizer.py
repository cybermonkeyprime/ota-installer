# src/decorators/colorizer.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

from src.styles.palette import Colors
from src.types.decorators import StringReturningDecorator

type R = str


@dataclass
class Colorizer(StringReturningDecorator):
    """
    Colorizer decorator — applies ANSI style to the result of string-returning
    functions.
    """

    style: str = field(default="")
    color_palette: Colors = field(default_factory=Colors)

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            try:
                result = function(*args, **kwargs)
                styled_result = (
                    f"{self.apply_style_prefix()}"
                    f"{result}"
                    f"{self.apply_style_suffix()}"
                )
            except AttributeError as error:
                raise ValueError("Invalid style attribute: ") from error
            return styled_result

        return cast(Callable[P, R], wrapper)

    def apply_style_prefix(self):
        return self.fetch_style_code(self.style)

    def apply_style_suffix(self):
        return self.fetch_style_code("reset")

    def fetch_style_code(self, style_name):
        try:
            return getattr(self.color_palette, style_name)
        except AttributeError as err:
            raise ValueError(
                f"Style '{style_name}' not found in color palette."
            ) from err


if __name__ == "__main__":
    # Example usage
    colorizer = Colorizer(style="task")

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))
