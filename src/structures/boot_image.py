from dataclasses import dataclass
from pathlib import Path

from src.paths.constants import BootImagePaths


@dataclass
class BootImageStruct(object):
    parent_directory: Path

    @property
    def stock(self) -> Path:
        return BootImagePaths.STOCK.value

    @property
    def magisk(self) -> Path:
        return BootImagePaths.MAGISK.value

    def __str__(self) -> str:
        return str(self.parent_directory)


@dataclass
class BootImage(BootImageStruct):
    pass
