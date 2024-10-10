from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable

from . import Colorizer, Indent, Printer  # Wrapper as DoubleWrapper


@dataclass
class HeaderWrapper:
    message: str = field(default="")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            self.message_output()
            result = function(*args, **kwargs)
            return result

        return inner

    @Printer(color=True)
    @Colorizer(style="variable")
    @Indent(interval=1)
    def message_output(self) -> Any:
        return f"{self.message}"
