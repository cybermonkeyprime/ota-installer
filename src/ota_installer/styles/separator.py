# src/ota_installer/styles/separator.py
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

from ota_installer.styles.indentation import indentation

SeparatorContainer = namedtuple(
    "SeparatorContainer", ["character", "spacing", "interval"]
)


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
