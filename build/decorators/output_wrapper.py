from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.styles import Indentation


@dataclass
class OutputWrapper:
    indent: int
    char: str = " "
    begin: str = ""
    end: str = ""
    style: str = ""

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            print(f"{self.beginning()}{result}{self.ending()}")
            return result

        return wrapper

    #        @IndentString(char=self.char[0], interval=self.indent)
    def indentation(self) -> str:
        return f"{Indentation(char=self.char[0], interval=self.indent)}"

    def beginning(self) -> str:
        return f"{self.begin}{self.indentation()}{self.style}"

    def ending(self) -> str:
        return f"{self.end}"
