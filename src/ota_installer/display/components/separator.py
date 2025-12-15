# src/ota_installer/display/components/separator.py
from dataclasses import dataclass, field

from rich.control import Control

from ...styles import Separator

from ..templates.display_template import (
    DisplayComponent,
)


@dataclass
class _Separator(DisplayComponent):
    """A class representing a separator component in a display."""

    indent: int = field(default=0)
    char: str = field(default="")

    def return_display(self) -> Separator:
        """
        Creates and returns a styles.Separator object with the current indent
            and char.
        """
        return Separator(self.indent, self.char)

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
        component = _Separator(self.indent, self.char[0])
        return f"{component.get_display()}> "
