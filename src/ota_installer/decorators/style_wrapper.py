# src/ota_installer/decorators/style_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast


@dataclass
class StyleWrapper(object):
    style: str = ""
    newline: bool = False

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            print(f"{self.style}{result}", end=self.new_line())
            return result

        return cast(Callable[P, R], wrapper)

    def new_line(self) -> str:
        return "\n" if self.newline else ""
