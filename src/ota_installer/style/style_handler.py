# src/ota_installer/style/style_handler.py
from dataclasses import dataclass
from enum import StrEnum


class RichColors(StrEnum):
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

    def tag(self, closing: bool = False) -> str:
        """Constructs the tag for the rich style."""
        return f"[/{self.value}]" if closing else f"[{self.value}]"

    def beginning(self):
        """Constructs the beginning tag for the rich style."""
        return self.tag()

    def ending(self):
        """Constructs the ending tag for the rich style."""
        return self.tag(closing=True)


@dataclass(frozen=True, slots=True)
class StyleContainer:
    """Container for style attributes."""

    character: str
    spacing: int
    interval: int

    def __call__(self) -> str:
        """Creates an indentation string."""
        return self.character * self.spacing * self.interval


SEPARATOR = StyleContainer(character="-", spacing=4, interval=10)


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    """Creates an indentation string."""
    return StyleContainer(char[0], spaces, interval)()


def separator(cls: StyleContainer = SEPARATOR) -> str:
    """Generates a formatted separator string."""
    return cls()


# Signed off by Brian Sanford on 20260527
