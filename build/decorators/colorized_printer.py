from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.decorators import Colorizer, Printer


@dataclass
class ColorizedPrinter:
    begin: str = ""
    end: str = ""
    style: str = "variable"

    def __call__(self, function: Callable) -> Any:
        @Printer(use_color=False)
        @Colorizer(style=self.style)
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return f"{result}"

        return inner
