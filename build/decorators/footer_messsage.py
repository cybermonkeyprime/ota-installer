from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.styles import Colors, Indentation


class Decorator:
    @dataclass
    class FooterMessage:
        text: str = "Finishing"
        indent: int = 0

        def __call__(self, function: Callable) -> Any:
            @wraps(function)
            def inner(*args: Any, **kwargs: Any) -> Any:
                result = function(*args, **kwargs)
                self.colorize_output()
                return result

            return inner

        def colorize_output(self) -> None:
            print("")
            print(
                f"{Colors.warning}{self.indentation()}{
                  self.text}{Colors.default}\n"
            )

        def indentation(self) -> str:
            return f"{Indentation(interval=self.indent)}"
