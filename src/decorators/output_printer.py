# src/decorators/output_printer.py
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import cast

from rich.console import Console

console = Console()


@dataclass
class OutputPrinter(object):
    prefix: str = field(default="")
    use_color: bool = field(default=False)
    suffix: str = field(default="\n")
    color: str = field(default="non_error")

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            from src.styles import RichColors

            style = RichColors[self.color.upper()]

            try:
                result = function(*args, **kwargs)
                console.print(
                    f"{style.beginnning()}{self.prefix}{result}{style.ending()}",
                    highlight=False,
                    end=self.suffix,
                )
                return result
            except Exception as e:
                raise RuntimeError(
                    f"An error occurred while executing the function: {e}"
                ) from e

        return cast(Callable[P, R], wrapper)
