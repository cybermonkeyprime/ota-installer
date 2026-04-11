# src/ota_installer/styles/separator.py
from enum import Enum

from .indentation import indentation


class SeparatorType(Enum):
    """Enumeration for separator constants."""

    CHAR = "-"
    SPACING = 4
    INTERVAL = 10


def separator(cls=SeparatorType) -> str:
    """Generates a formatted separator string."""
    return indentation(
        char=cls.CHAR.value,
        spaces=cls.SPACING.value,
        interval=cls.INTERVAL.value,
    )


# Signed off by Brian Sanford on 20260410
