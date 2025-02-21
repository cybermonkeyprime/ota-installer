from dataclasses import dataclass


@dataclass
class Indentation:
    interval: int
    char: str = " "
    spacing: int = 4

    def __str__(self):
        return f"{self.char[0] * self.spacing * self.interval}"
