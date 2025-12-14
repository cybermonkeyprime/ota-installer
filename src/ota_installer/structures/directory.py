# src/ota_installer/structures/directory.py
from dataclasses import dataclass, field
from pathlib import Path

from .boot_image import BootImage
from .magisk import MagiskStruct


@dataclass
class Directory(object):
    ota: str
    _boot_image: Path = field(repr=False)
    boot_image: BootImage = field(init=False)
    magisk: MagiskStruct = field(init=False)

    def __post_init__(self) -> None:
        self.boot_image = BootImage(self._boot_image)
        self.magisk = MagiskStruct()

    def __str__(self) -> str:
        return str(self._boot_image)
