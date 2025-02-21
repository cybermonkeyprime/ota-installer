from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from build.decorators import Colorizer, Indent, Printer  # Wrapper as DoubleWrapper


@dataclass
class FooterWrapper:
    message: str = field(default="")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            self.message_output()
            return result

        return inner

    @Printer(use_color=True)
    @Colorizer(style="info")
    @Indent(interval=1)
    def message_output(self) -> Any:
        return f"{self.message}"
