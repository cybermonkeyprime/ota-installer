# src/ota_installer/dispatchers/constants/directory_type_constants.py
from enum import Enum


class DirectoryTypeConstants(Enum):
    STOCK = "stock"
    MAGISK = "magisk"
    LOCAL = "local"
    REMOTE = "remote"

    def __str__(self) -> str:
        return self.value
