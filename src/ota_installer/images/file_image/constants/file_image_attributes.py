# src/ota_installer/images/file_image/constants/file_image_attributes.py
from enum import Enum
from typing import Self

from ....images.boot_image.constants.boot_image_paths import BootImagePaths
from ..constants.file_image_names import FileImageNames
from ..containers.file_image_container import (
    FileImageStruct,
)


class FileImageAttributes(Enum):
    PAYLOAD = FileImageStruct(
        title=FileImageNames.PAYLOAD.value, extension="bin"
    )
    STOCK = FileImageStruct(title="boot", extension="img")
    MAGISK = FileImageStruct(
        title=FileImageNames.MAGISK.value, extension="img"
    )

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
