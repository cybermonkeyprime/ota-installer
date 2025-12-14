# src/ota_installer/display/components/separator.py
from dataclasses import dataclass, field

from rich.control import Control

import src.ota_installer.styles as styles
from src.ota_installer.display.templates.display_template import (
    DisplayComponent,
)


@dataclass
class Separator(DisplayComponent):
    """A class representing a separator component in a display."""

    indent: int = field(default=0)
    char: str = field(default="")

    def return_display(self) -> styles.Separator:
        """
        Creates and returns a styles.Separator object with the current indent
            and char.
        """
        return styles.Separator(self.indent, self.char)

    def get_display(self) -> object:
        """The display representation of the separator."""
        return self.return_display()


@dataclass
class DisplaySeparator(object):
    """
    A class for creating a display separator with a specified indentation and
        character.
    """

    indent: int = field(default=9)
    char: str = field(default="-")

    def move_cursor_up(self) -> str:
        return str(Control.move(y=-1))

    def __str__(self) -> str:
        """Returns a string representation of the display separator."""
        component = Separator(self.indent, self.char[0])
        return f"{component.get_display()}> "
