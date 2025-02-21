from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from rich import print as rprint

from build.styles import Colors, Indentation


@dataclass
class PrettyOutputWrapper:
    indent: int
    char: str = " "
    begin: str = ""
    end: str = ""
    style: str = ""

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            rprint(f"{self.beginning()}{result}{self.ending()}")
            return result

        return wrapper

    def indentation(self) -> str:
        return f"{Indentation(char=self.char[0], interval=self.indent)}"

    def beginning(self) -> str:
        style = eval(f"Colors.{self.style}")
        return f"{style}{self.begin}{self.indentation()}"

    def ending(self) -> str:
        return f"{self.end}{Colors.default}"
