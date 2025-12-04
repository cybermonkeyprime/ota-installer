# src/decorators/figletizer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from pyfiglet import figlet_format

from src.types.decorators import StringReturningDecorator

type R = str


@dataclass
class Figletizer(StringReturningDecorator):
    font: str = "slant"

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{figlet_format(str(result), font=self.font)}"

        return cast(Callable[P, R], wrapper)
