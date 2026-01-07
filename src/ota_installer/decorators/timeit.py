# src/ota_installer/decorators/timeit.py
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class TimeIt(GenericDecorator):
    start_time: float = 0
    end_time: float = 0

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self.start_time = self.time_counter()
            result = function(*args, **kwargs)
            self.end_time = self.time_counter()
            function_str = f"{function.__name__}{args} {kwargs}"
            total_time = f"{self.total_time():.4} seconds"
            print(f"Function {function_str} Took {total_time}")
            return result

        return cast(Callable[P, R], wrapper)

    def time_counter(self) -> float:
        return time.perf_counter()

    def total_time(self) -> float:
        return self.end_time - self.start_time
