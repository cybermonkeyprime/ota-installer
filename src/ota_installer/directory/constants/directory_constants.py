# src/ota_installer/dispatchers/constants/_directory_type_mapping.py
from enum import Enum


class DirectoryConstants(Enum):
    STOCK = "stock"
    MAGISK = "magisk"
    LOCAL = "local"
    REMOTE = "remote"

    def __str__(self) -> str:
        return self.value
