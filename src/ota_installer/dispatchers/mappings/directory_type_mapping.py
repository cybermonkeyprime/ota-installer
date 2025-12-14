from enum import Enum


class DirectoryTypeMapping(Enum):
    STOCK = "stock"
    MAGISK = "magisk"
    LOCAL = "local"
    REMOTE = "remote"

    def __str__(self) -> str:
        return self.value
