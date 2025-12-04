from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BootImagePath(Enum):
    STOCK = "stock"
    MAGISK = "magisk"

    def path(self, path: Path) -> Path:
        return Path.home() / path / self.value


@dataclass
class BootImage(object):
    parent_directory: Path

    @property
    def stock(self) -> Path:
        return BootImagePath.STOCK.path(self.parent_directory)

    @property
    def magisk(self) -> Path:
        return BootImagePath.MAGISK.path(self.parent_directory)

    def __str__(self) -> str:
        return str(self.parent_directory)


@dataclass
class BootImageStruct(object):
    parent_directory: Path

    @property
    def stock(self) -> Path:
        return BootImagePath.STOCK.path(self.parent_directory)

    @property
    def magisk(self) -> Path:
        return BootImagePath.MAGISK.path(self.parent_directory)

    def __str__(self) -> str:
        return str(self.parent_directory)
