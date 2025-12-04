# src/decorators/output_printer.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast


@dataclass
class OutputPrinter(object):
    prefix: str = field(default="")
    use_color: bool = field(default=False)
    suffix: str = field(default="\n")
    color: str | None = field(default=None)

    def __post_init__(self):
        from src.styles import Colors

        if self.use_color and self.color is None:
            self.color = Colors.variable  # Default color

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            from src.styles import Colors

            try:
                result = function(*args, **kwargs)
                color_prefix = self.color if self.use_color else ""
                color_suffix = Colors.reset if self.use_color else ""
                print(
                    f"{color_prefix}{self.prefix}{result}{color_suffix}",
                    end=self.suffix,
                )
                return result
            except Exception as e:
                raise RuntimeError(
                    f"An error occurred while executing the function: {e}"
                ) from e

        return cast(Callable[P, R], wrapper)
