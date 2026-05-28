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
class SeparatorType:
    """Container for separator constants."""

    CHAR = "-"
    SPACING = 4
    INTERVAL = 10


@dataclass(frozen=True, slots=True)
class StyleContainer:
    """Container for style attributes."""

    character: str
    spacing: int
    interval: int


def indentation(interval: int = 1, char: str = " ", spaces: int = 4) -> str:
    """Creates an indentation string."""
    style = StyleContainer(
        interval=interval, character=char[0], spacing=spaces
    )
    return style.character * style.spacing * style.interval


def separator(cls: type[SeparatorType] = SeparatorType) -> str:
    """Generates a formatted separator string."""
    return indentation(
        char=cls.CHAR, spaces=cls.SPACING, interval=cls.INTERVAL
    )


# Signed off by Brian Sanford on 20260527
