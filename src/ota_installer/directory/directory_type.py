# src/ota_installer/directory/directory_type.py
from enum import Enum, StrEnum, auto
from pathlib import Path


class DirectoryType(StrEnum):
    """Enumeration for directory types used in OTA installation."""

    STOCK = auto()
    MAGISK = auto()
    LOCAL = auto()
    REMOTE = auto()

    @classmethod
    def to_dict(cls, data: "VariableDirector") -> dict[Enum, Path]:
        """Creates a directory collection from the boot image."""
        boot_image = data.directory.boot_image
        magisk_image = data.directories.magisk

        boot_dict = {
            cls[name.upper()]: getattr(boot_image, name)
            for name in ["stock", "magisk"]
        }
        magisk_dict = {
            cls[name.upper()]: Path(getattr(magisk_image, f"{name}_path"))
            for name in ["local", "remote"]
        }

        return {**boot_dict, **magisk_dict}

    def get_path(self, obj) -> Path:
        return self.to_dict(obj)[self]


# Signed off by Brian Sanford on 20260827
