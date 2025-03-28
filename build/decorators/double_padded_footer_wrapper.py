from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from build.decorators import Colorizer, Indent, Printer


@dataclass
class DoublePaddedFooterWrapper:
    message: str = field(default="Finished!")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            self.string_output("")
            self.string_output(self.message)
            self.string_output("")
            return result

        return inner

    @Printer(use_color=True)
    @Colorizer(style="warning")
    @Indent(interval=1)
    def string_output(self, message) -> str:
        return f"{message}"


if __name__ == "__main__":
    pass
