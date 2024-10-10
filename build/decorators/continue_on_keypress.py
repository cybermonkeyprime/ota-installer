from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, TypeVar

from build.styles.indentation import Indentation

from .colorizer import Colorizer
from .printer import Printer

# Define a generic type for the decorator
T = TypeVar("T", bound=Callable[..., Any])


@dataclass
class ContinueOnKeyPress:
    indent: int = field(default=1)
    char: str = field(default=" ")

    def __call__(self, function: T) -> T:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = function(*args, **kwargs)
                self.display_message()
                input()
                return result
            except Exception as error:
                raise RuntimeError(f"An error occurred: {error}")

        return wrapper  # type: ignore

    def create_indentation(self) -> str:
        return str(Indentation(char=self.char[0], interval=self.indent))

    @Printer(prefix="\n", suffix="")
    @Colorizer(style="title")
    def display_message(self) -> str:
        message = "Press the Enter key to continue... "
        return message


if __name__ == "__main__":
    pass
