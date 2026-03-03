# src/ota_installer/dispatchers/constants/_directory_type_mapping.py
from enum import StrEnum, auto


class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()


