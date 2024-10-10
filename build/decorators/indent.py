from dataclasses import dataclass
from typing import Any
from build.styles.indentation import Indentation


@dataclass
class Indent:
    interval: int = 0
    char = " "

    def __call__(self, function) -> Any:
        def inner(*args, **kwargs):
            result = function(*args, **kwargs)
            return f"{self.indent()}{result}"

        return inner

    def indent(self):
        return f"{Indentation(char=self.char, interval=self.interval)}"
