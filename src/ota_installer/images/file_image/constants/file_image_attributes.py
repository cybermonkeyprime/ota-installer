# src/ota_installer/images/file_image/constants/file_image_attributes.py
from enum import Enum
from pathlib import Path
from typing import Self

from ....images.boot_image.constants.boot_image_paths import BootImagePaths
from ..constants.file_image_names import FileImageNames


class FileImageAttributes(Enum):
    """
    Enumeration to describe file image attributes with associated metadata.
    """

    PAYLOAD = (FileImageNames.PAYLOAD.value, "bin")
    STOCK = ("boot", "img")
    MAGISK = (FileImageNames.MAGISK.value, "img")

    def __init__(self, title: str, extension: str):
        self.title = title
        self.extension = extension
        self.device = ""
        self.version = ""

    @property
    def file_name(self) -> str:
        """Generates the formatted file name based on attributes."""
        return f"{self.device}-{self.title}-{self.version}.{self.extension}"

    def set_device(self, device: str) -> Self:
        """Sets the device attribute and returns the enum instance."""
        self.device = str(device)
        return self

    def set_version(self, version: str) -> Self:
        """Sets the version attribute and returns the enum instance."""
        self.version = str(version)
        return self

    def set_file_path(self) -> Path:
        """Constructs the full file path for the image file."""
        boot_image_path = BootImagePaths[self.name].value
        return Path(boot_image_path) / self.file_name
        # Signed off by Brian Sanford on 20260108
