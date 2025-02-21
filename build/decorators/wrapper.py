from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import Any

from build.decorators import Colorizer, Indent, Printer


@dataclass
class Wrapper:
    meessage: str = field(default="")

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            self.string_output()
            result = function(*args, **kwargs)
            self.string_output()
            return result

        return inner

    @Printer(use_color=False)
    @Colorizer(style="variable")
    @Indent(interval=1)
    def string_output(self) -> None:
        print(f"{self.meessage}")


if __name__ == "__main__":
    pass
