from dataclasses import dataclass
from .indentation import Indentation


@dataclass
class Separator:
    increment: int = 1
    char: str = "-"

    def __str__(self) -> str:
        return f"{Indentation(char=self.char[0], interval=self.increment)}"
