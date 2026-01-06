# src/ota_installer/styles/separator.py
from dataclasses import dataclass
from enum import Enum

from .indentation import indentation


class SeparatorConstants(Enum):
    CHAR = "-"
    SPACING = 4
    INTERVAL = 10


@dataclass
class Separator(object):
    increment: int = 1
    char: str = "-"

    @property
    def data(self) -> list:
        return [enum_member.value for enum_member in SeparatorConstants]

    def __str__(self) -> str:
        sc = SeparatorConstants
        return indentation(
            char=sc.CHAR.value,
            spaces=sc.SPACING.value,
            interval=sc.INTERVAL.value,
        )


def separator(increment: int = 1, char: str = "-") -> str:
    sc = SeparatorConstants
    return indentation(
        char=sc.CHAR.value,
        spaces=sc.SPACING.value,
        interval=sc.INTERVAL.value,
    )
