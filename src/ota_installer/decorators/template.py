# src/ota_installer/decorators/template.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from ..protocols.decorator_protocols import GenericDecorator

type R = object


@dataclass
class Example(GenericDecorator):
    func: Callable

    def __call__[**P](self, *args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Beginning {self.func.__name__}")
        result = self.func(*args, **kwargs)
        print(f"Ending {self.func.__name__}")
        return cast(Callable[P, R], result)


@dataclass
class ExampleWithArgs(GenericDecorator):
    begin: str = "Beginning"
    end: str = "Ending"

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"{self.begin} {function.__name__}")
            result = function(*args, **kwargs)
            print(f"{self.end} {function.__name__}")
            return result

        return cast(Callable[P, R], wrapper)
