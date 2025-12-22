# src/ota_installer/boot_image/containers/boot_image.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.paths.boot_image_paths import BootImagePaths


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
