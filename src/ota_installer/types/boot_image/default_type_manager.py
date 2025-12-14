# src/ota_installer/types/boot_image/default_type_manager.py
from collections import namedtuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from ...paths.constants.boot_image_paths import BootImagePaths
from ...structures import FileNameParser, ImageFile

ImageAttributeTuple = namedtuple("AttributeTuple", ["title", "extension"])


class ImageAttributes(Enum):
    PAYLOAD = ImageAttributeTuple(title="payload", extension="bin")
    STOCK = ImageAttributeTuple(title="boot", extension="img")
    MAGISK = ImageAttributeTuple(title="magisk", extension="img")

    def set_file_name(self, device: str, version: str) -> str:
        return (
            f"{BootImagePaths[self.name].value}/"
            f"{device}-{self.value.title}-{version}.{self.value.extension}"
        )


# Centralized manager
@dataclass
class DefaultImageTypeManager(object):
    file_name_bits: FileNameParser
    path: str = field(default="")

    payload_image: ImageFile = field(init=False)
    stock_image: ImageFile = field(init=False)
    magisk_image: ImageFile = field(init=False)

    def __post_init__(self):
        self.device = self.file_name_bits.device
        self.version = self.file_name_bits.version

        self.payload = self.create_image(ImageAttributes.PAYLOAD.value)
        self.stock = self.create_image(ImageAttributes.STOCK.value)
        self.magisk = self.create_image(ImageAttributes.MAGISK.value)

    def create_image(self, data: tuple) -> ImageFile:
        enum = "stock" if data.title == "boot" else data.title
        path = Path(
            ImageAttributes[enum.upper()].set_file_name(
                self.device, self.version
            )
        )
        return ImageFile(file_path=Path(path.name), directory_path=path.parent)


# Optional test function
def create_file_name_parser(variable: Path) -> FileNameParser:
    return FileNameParser(variable)
