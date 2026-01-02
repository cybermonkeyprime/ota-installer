# src/ota_installer/display/components/separator.py
from dataclasses import dataclass, field

from rich.control import Control

from ...styles import separator


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
        get_display = separator(self.indent, self.char[0])
        return f"{get_display}> "
