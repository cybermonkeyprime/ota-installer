# src/ota_installer/decorators/timeit.py
import time
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import cast

from .protocols.decorator_protocols import GenericDecorator


@dataclass
class TimeIt(GenericDecorator):
    """Decorator to measure the execution time of a function."""

    start_time: float = 0
    end_time: float = 0

    def __call__[R, **P](self, function: Callable[P, R]) -> Callable[P, R]:
        """Wrap the function to measure its execution time."""

        @wraps(function)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            self.start_time = self._get_current_time()
            result = function(*args, **kwargs)
            self.end_time = self._get_current_time()
            self._log_execution_time(function, args, kwargs)
            return result

        return cast(Callable[P, R], wrapper)

    def _log_execution_time(
        self, function: Callable, args: tuple, kwargs: dict
    ) -> None:
        """Log the execution time of the function."""
        total_time = self._calculate_total_time()
        function_signature = f"{function.__name__}{args} {kwargs}"
        print(f"Function {function_signature} took {total_time:.4f} seconds")

    def _get_current_time(self) -> float:
        """Get the current time in seconds."""
        return time.perf_counter()

    def _calculate_total_time(self) -> float:
        """Calculate the total execution time."""
        return self.end_time - self.start_time


