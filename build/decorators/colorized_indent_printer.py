from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any

from build.decorators.colorizer import Colorizer
from build.decorators.indent import Indent
from build.decorators.printer import Printer

"""
Do not use this causes circlular import
circular until resolved
from build.decorators import Colorizer, Indent, Printer
"""


@dataclass
class ColorizedIndentPrinter:
    indent: int = 0
    begin: str = ""
    end: str = ""
    style: str = "variable"

    def __call__(self, function: Callable) -> Any:
        @Printer(use_color=True)
        @Colorizer(style=self.style)
        @Indent(interval=self.indent)
        @wraps(function)
        def inner(*args: Any, **kwargs: Any) -> Any:
            result = function(*args, **kwargs)
            return result

        return inner
