# src/ota_installer/styles/separator.py
from enum import Enum

from .indentation import indentation


class SeparatorConstants(Enum):
    """Enumeration for separator constants."""

    CHAR = "-"
    SPACING = 4
    INTERVAL = 10


def separator(
    increment: int = 1, char: str = SeparatorConstants.CHAR.value
) -> str:
    """Generates a formatted separator string."""
    sc = SeparatorConstants
    return indentation(
        char=sc.CHAR.value,
        spaces=sc.SPACING.value,
        interval=sc.INTERVAL.value,
    )


# Signed off by Brian Sanford on 20260119
