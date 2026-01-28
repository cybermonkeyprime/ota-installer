# src/ota_installer/decorators/template.py
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator

type R = object


@dataclass
class Example(GenericDecorator):
    """A decorator class that logs the start and end of function execution."""

    func: Callable
    start_message: str = "Beginning"
    end_message: str = "Ending"

    def __call__[**P](self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Wraps the function to log messages before and after execution."""
        print(f"{self.start_message} {self.func.__name__}")
        result = self.func(*args, **kwargs)
        print(f"{self.end_message} {self.func.__name__}")
        return cast(Callable[P, R], result)


@dataclass
class ExampleWithArgs(GenericDecorator):
    """A decorator class that logs the start and end of function execution."""

    begin: str = "Beginning"
    end: str = "Ending"

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wraps the function to log messages before and after execution."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"{self.begin} {function.__name__}")
            result = function(*args, **kwargs)
            print(f"{self.end} {function.__name__}")
            return result

        return cast(Callable[P, R], wrapper)


