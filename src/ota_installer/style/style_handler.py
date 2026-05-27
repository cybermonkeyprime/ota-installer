from dataclasses import dataclass
from enum import Enum, StrEnum


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

    def beginning(self):
        """Constructs the beginning tag for the rich style."""
        return self.tag()

    def ending(self):
        """Constructs the ending tag for the rich style."""
        return self.tag(closing=True)

    def tag(self, closing: bool = False) -> str:
        """Constructs the tag for the rich style."""
        return f"[/{self.value}]" if closing else f"[{self.value}]"


class SeparatorType(Enum):
    """Enumeration for separator constants."""

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
    style_container = StyleContainer(
        interval=interval, character=char[0], spacing=spaces
    )
    return (
        style_container.character
        * style_container.spacing
        * style_container.interval
    )


def separator(cls: type[SeparatorType] = SeparatorType) -> str:
    """Generates a formatted separator string."""
    return indentation(
        char=cls.CHAR.value,
        spaces=cls.SPACING.value,
        interval=cls.INTERVAL.value,
    )
