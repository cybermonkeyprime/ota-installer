# src/decorators/colorized_printer.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from src.types.decorators import GenericDecorator

type R = str


@dataclass
class ColorizedOutputPrinter(GenericDecorator):
    begin: str = ""
    end: str = ""
    style: str = "variable"

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        from . import Colorizer, OutputPrinter

        @OutputPrinter(use_color=False)
        @Colorizer(style=self.style)
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{result}"

        return cast(Callable[P, R], wrapper)
