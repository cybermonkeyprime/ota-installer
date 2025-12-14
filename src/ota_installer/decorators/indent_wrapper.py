# /src/ota_installer/decorators/indent_wrapper.py
from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

from src.ota_installer.styles.indentation import Indentation
from src.ota_installer.types.decorators import StringReturningDecorator

type R = str


@dataclass
class IndentWrapper(StringReturningDecorator):
    interval: int = 0
    char = " "

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{self.indent()}{result}"

        return cast(Callable[P, R], wrapper)

    def indent(self):
        return f"{Indentation(char=self.char, interval=self.interval)}"
