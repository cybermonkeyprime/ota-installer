# src/ota_installer/styles/separator.py
from dataclasses import dataclass
from enum import Enum


class SeparatorConstants(Enum):
    CHAR = "-"
    SPACING = 4
    INDENT = 10


@dataclass
class Separator(object):
    increment: int = 1
    char: str = "-"

    def __str__(self) -> str:
        constants = SeparatorConstants
        return f"{constants.CHAR.value[0] * constants.SPACING.value * constants.INDENT.value}"
