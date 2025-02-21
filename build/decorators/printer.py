from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Optional, TypeVar, cast

from build.styles import Colors

# Define a generic type for functions
F = TypeVar("F", bound=Callable[..., Any])


@dataclass
class Printer:
    prefix: str = field(default="")
    use_color: bool = field(default=False)
    suffix: str = field(default="\n")
    color: Optional[str] = field(default=None)

    def __post_init__(self):
        if self.use_color and self.color is None:
            self.color = Colors.warning  # Default color

    def __call__(self, function: F) -> F:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = function(*args, **kwargs)
                color_prefix = self.color if self.use_color else ""
                color_suffix = Colors.default if self.use_color else ""
                print(
                    f"{color_prefix}{self.prefix}{result}{color_suffix}",
                    end=self.suffix,
                )
                return result
            except Exception as e:
                raise RuntimeError(
                    f"An error occurred while executing the function: {e}"
                )

        return cast(F, wrapper)
