from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any


class Decorator:
    @dataclass
    class WrapperTemplate:
        def __call__(self, function: Callable) -> Any:
            @wraps(function)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                result = function(*args, **kwargs)
                return result

            return wrapper
