# src/styles/palette.py
from enum import Enum


class RichColors(Enum):
    TITLE = "green bold"
    AUTHOR = "white"
    VERSION = "yellow"
    SEPARATOR = "green bold"
    TASK = "green bold"
    VARIABLE = "yellow"
    ERROR = "red bold"
    WARNING = "yellow"
    NON_ERROR = "white"

    def beginnning(self):
        return f"[{self.value}]"

    def ending(self):
        return f"[/{self.value}]"


def main() -> None:
    pass


if __name__ == "__main__":
    main()
