from dataclasses import dataclass
from functools import wraps


@dataclass
class MultiplyString:
    interval: int = 0

    def __call__(self, function):
        @wraps(function)
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            return f"{result * self.interval}"

        return inner
