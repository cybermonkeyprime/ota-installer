import time
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


@dataclass
class TimeIt:
    start_time: float = 0
    end_time: float = 0

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.start_time = self.time_counter()
            result = function(*args, **kwargs)
            self.end_time = self.time_counter()
            function_str = f"{function.__name__}{args} {kwargs}"
            total_time = f"{self.total_time():.4} seconds"
            print(f"Function {function_str} Took {total_time}")
            return result

        return wrapper

    def time_counter(self) -> float:
        return time.perf_counter()

    def total_time(self) -> float:
        return self.end_time - self.start_time
