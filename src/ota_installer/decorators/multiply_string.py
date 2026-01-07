# src/ota_installer/decorators/multiply_string.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator

type R = str


@dataclass
class MultiplyString(GenericDecorator):
    interval: int = 0

    def __call__[**P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            result = function(*args, **kwargs)
            return f"{str(result) * self.interval}"

        return cast(Callable[P, R], wrapper)
