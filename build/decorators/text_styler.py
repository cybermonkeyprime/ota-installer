from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from build.styles import Colors


@dataclass
class TextStyler:
    style: str = field(default="blue")

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> str:
            result = function(*args, **kwargs)
            return f"{self.get_style_code()}{result}{Colors.default}"

        return wrapped_function

    def get_style_code(self) -> str:
        try:
            return getattr(Colors, self.style)
        except AttributeError:
            return "blue"


# Usage example:
# Assuming Colors class is defined with color attributes like Colors.blue, Colors.red, etc.

if __name__ == "__main__":

    @TextStyler(style="red")
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))
