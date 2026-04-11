# src/ota_installer/dispatchers/constants/_directory_type_mapping.py
from enum import StrEnum, auto
from pathlib import Path


class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def mapping(cls, obj: type) -> dict:
        """Creates a directory collection from the boot image."""
        boot_image = obj.directory.boot_image
        magisk_image = obj.directories.magisk
        return {
            cls.STOCK: Path(boot_image.stock),
            cls.MAGISK: Path(boot_image.magisk),
            cls.LOCAL: Path(magisk_image.local_path),
            cls.REMOTE: Path(magisk_image.remote_path),
        }


# Signed off by Brian Sanford on 20260410
