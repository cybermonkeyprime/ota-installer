from dataclasses import dataclass
from functools import wraps
from pyfiglet import figlet_format


@dataclass
class Figletizer:
    font: str = "slant"

    def __call__(self, function):
        @wraps(function)
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            return f"{figlet_format(result, font=self.font)}"

        return inner
