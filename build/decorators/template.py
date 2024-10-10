from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable


@dataclass
class DecoratorTemplate:
    @dataclass
    class Example:
        func: Callable

        def __call__(self, *args: Any, **kwargs: Any) -> Any:
            print(f"Beginning {self.func.__name__}")
            result = self.func(*args, **kwargs)
            print(f"Ending {self.func.__name__}")
            return result

    @dataclass
    class ExampleWithArgs:
        begin: str = "Beginning"
        end: str = "Ending"

        def __call__(self, func: Callable) -> Any:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                print(f"{self.begin} {func.__name__}")
                result = func(*args, **kwargs)
                print(f"{self.end} {func.__name__}")
                return result

            return wrapper
