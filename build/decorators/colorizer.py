from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from build.styles import Colors


@dataclass
class Colorizer(object):
    style: str = field(default="default")
    color_palette: Colors = field(default_factory=Colors)

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> str:
            try:
                result = function(*args, **kwargs)
                styled_result = f"{self.styling}{result}"
                # {self.suffix_style}"
            except AttributeError as error:
                raise AttributeError(f"Invalid style attribute: {error}")
            return styled_result

        return wrapped_function

    @property
    def styling(self):
        return getattr(self.color_palette, self.style, "default")


if __name__ == "__main__":
    # Example usage
    colorizer = Colorizer(style="info")

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))
