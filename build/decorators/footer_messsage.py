from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from build.styles.palette import Colors
from build.styles.indentation import Indentation


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
                f"{Colors.task}{self.indentation()}{
                  self.text}{Colors.reset}\n"
            )

        def indentation(self) -> str:
            return f"{Indentation(interval=self.indent)}"
