from dataclasses import dataclass
from build.styles.indentation import Indentation


@dataclass
class Separator:
    increment: int = 1
    char: str = "-"

    def __str__(self) -> str:
        return f"{Indentation(char=self.char[0], interval=self.increment)}"
        # return f"{self.char * 4 * self.increment}"
