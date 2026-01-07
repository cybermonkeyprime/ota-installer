# src/ota_installer/decorators/encapsulation.py
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


class SeparatorSpecs(Enum):
    CHAR = "="
    SPACING = 4
    INTERVAL = 20


@dataclass
class Encapsulate(GenericDecorator):
    from .multiply_string import MultiplyString
    from .output_printer import OutputPrinter

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self.separator()
            result = function(*args, **kwargs)
            self.separator()
            return result

        return cast(Callable[P, R], wrapper)

    @OutputPrinter(prefix="\n", suffix="\n\n")
    @MultiplyString(
        interval=(SeparatorSpecs.SPACING.value * SeparatorSpecs.INTERVAL.value)
    )
    def separator(self) -> str:
        return SeparatorSpecs.CHAR.value
