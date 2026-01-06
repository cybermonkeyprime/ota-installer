# src/ota_installer/styles/separator.py
from enum import Enum

from .indentation import indentation


class SeparatorConstants(Enum):
    CHAR = "-"
    SPACING = 4
    INTERVAL = 10


def separator(increment: int = 1, char: str = "-") -> str:
    sc = SeparatorConstants
    return indentation(
        char=sc.CHAR.value,
        spaces=sc.SPACING.value,
        interval=sc.INTERVAL.value,
    )
