# src/ota_installer/display/components/separator.py
from rich.control import Control

from ...styles import separator


def display_separator(indent=9, char="-") -> str:
    """Returns a string representation of the display separator."""
    get_display = separator(indent, char[0])
    return f"{get_display}> "
