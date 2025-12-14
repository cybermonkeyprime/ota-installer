# src/paths/constants/image_file_attributes.py
from collections import namedtuple
from enum import Enum
from typing import Self

from .boot_image_paths import BootImagePaths

ImageFileStruct = namedtuple("ImageFileStruct", ["title", "extension"])


class ImageFileAttributes(Enum):
    PAYLOAD = ImageFileStruct(title="payload", extension="bin")
    STOCK = ImageFileStruct(title="boot", extension="img")
    MAGISK = ImageFileStruct(title="magisk", extension="img")

    def set_device(self, device: str) -> Self:
        self.device = str(device)
        return self

    def set_version(self, version: str) -> Self:
        self.version = str(version)
        return self

    def set_file_path(self) -> str:
        return (
            f"{BootImagePaths[self.name].value}/"
            f"{self.device}-{self.value.title}-{self.version}.{self.value.extension}"
        )
