from dataclasses import dataclass


@dataclass
class Indentation:
    interval: int
    char: str = " "
    spaces: int = 4

    def __str__(self):
        return f"{self.char[0] * self.spaces * self.interval}"
