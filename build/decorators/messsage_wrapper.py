from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.decorators import Colorizer, Printer


@dataclass
class MessageWrapper:
    begin: str = ""
    text: str = ""
    end: str = ""
    header: bool = False
    footer: bool = False
    style: str = "variable"

    def __call__(self, function: Callable) -> Any:
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            self._header()
            result = function(*args, **kwargs)
            self._footer()
            return result

        return inner

    @Printer()
    @Colorizer(style="title")
    def _header(self) -> str:
        return self.text if self.header else ""

    @Printer(prefix="\n", suffix="\n")
    @Colorizer(style="title")
    def _footer(self) -> str:
        return self.text if self.footer else ""

    def ending(self) -> str:
        return f"{self.end}"
