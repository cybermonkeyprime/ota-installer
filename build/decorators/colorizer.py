from dataclasses import dataclass, field
from typing import Callable, Any
from functools import wraps

from build.styles.palette import Colors


@dataclass
class Colorizer(object):
    style: str = field(default="")
    color_palette: Colors = field(default_factory=Colors)

    def __call__(self, function: Callable) -> Callable:
        @wraps(function)
        def wrapped_function(*args: Any, **kwargs: Any) -> str:
            try:
                result = function(*args, **kwargs)
                styled_result = (
                    f"{self.apply_style_prefix()}{result}{self.apply_style_suffix()}"
                )
            except AttributeError as error:
                raise ValueError(f"Invalid style attribute: {error}")
            return styled_result

        return wrapped_function

    def apply_style_prefix(self):
        return self.fetch_style_code(self.style)

    def apply_style_suffix(self):
        return self.fetch_style_code("reset")

    def fetch_style_code(self, style_name):
        try:
            return getattr(self.color_palette, style_name)
        except AttributeError:
            raise ValueError(f"Style '{style_name}' not found in color palette.")


if __name__ == "__main__":
    # Example usage
    colorizer = Colorizer(style="task")

    @colorizer
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))
