from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable

from . import Colorizer, Indent, Printer


@dataclass
class DoublePaddedFooterWrapper:
    begining: str = field(default="")
    message: str = field(default="Finished!")
    ending: str = field(default="")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            self.string_output(self.begining)
            self.string_output(self.message)
            self.string_output(self.ending)
            return result

        return inner

    @Printer(color=False)
    @Colorizer(style="variable")
    @Indent(interval=1)
    def string_output(self, message) -> str:
        return f"{message}"


if __name__ == "__main__":
    pass
