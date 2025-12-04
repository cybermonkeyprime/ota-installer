# src/decorators/colorized_figlet.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from src.types.decorators import GenericDecorator

from .colorizer import Colorizer
from .figletizer import Figletizer


@dataclass
class ColorizedFiglet(GenericDecorator):
    style: str = "variable"
    font: str = "slant"

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @Colorizer(style=self.style)
        @Figletizer(font=self.font)  # type: ignore[return-value]
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return result

        return cast(Callable[P, R], wrapper)
