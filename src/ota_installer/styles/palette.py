# src/ota_installer/styles/palette.py
from enum import Enum


class RichColors(Enum):
    """Enumeration for rich color styles."""

    TITLE = "green bold"
    AUTHOR = "white"
    VERSION = "yellow"
    SEPARATOR = "green bold"
    TASK = "green bold"
    VARIABLE = "yellow"
    ERROR = "red bold"
    WARNING = "yellow"
    NON_ERROR = "white"

    def beginning(self):
        """Constructs the beginning tag for the rich style."""
        return f"[{self.value}]"

    def ending(self):
        """Constructs the ending tag for the rich style."""
        return f"[/{self.value}]"


def main() -> None:
    """The main function of the module, provided for completeness."""
    pass


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260108
