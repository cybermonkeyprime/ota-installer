from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, TypeVar, cast, Optional
from colorama import Fore, Style

# Define a generic type for functions
F = TypeVar("F", bound=Callable[..., Any])


def catch_exceptions(function: F) -> F:
    """Decorator to catch and handle exceptions in a function."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(f"An error occurred: {e}")
            return None

    return cast(F, wrapper)


@dataclass
class ColoredPrinter:
    """
    A class that provides a printing functionality with an optional prefix,
    suffix, and color support.
    """

    prefix: str = field(default="")
    use_color: bool = field(default=False)
    suffix: str = field(default="\n")
    color: Optional[str] = field(default=None)

    def __post_init__(self):
        if self.use_color and self.color is None:
            self.color = Fore.GREEN  # Default color

    def __call__(self, function: F) -> F:
        """Decorator to print the result of a function with optional prefix and suffix."""

        @wraps(function)
        def decorated_function(*args, **kwargs) -> Any:
            result = function(*args, **kwargs)
            color_prefix = self.color if self.use_color else ""
            color_suffix = Style.RESET_ALL if self.use_color else ""
            print(f"{color_prefix}{self.prefix}{result}{
                  color_suffix}", end=self.suffix)
            return result

        return cast(F, decorated_function)

