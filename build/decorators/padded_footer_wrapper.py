from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable

from . import Colorizer, Indent, Printer


@dataclass
class PaddedFooterWrapper:
    padding: str = field(default="")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            self.padding_output()
            return result

        return inner

    @Printer(color=True)
    @Colorizer(style="variable")
    @Indent(interval=1)
    def padding_output(self) -> Any:
        return f"{self.padding}"
