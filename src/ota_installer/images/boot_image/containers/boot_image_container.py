# src/ota_installer/images/boot_image/containers/boot_image_conatiner.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.boot_image_paths import BootImagePaths


@dataclass
class BootImageContainer(object):
    """Container for boot image paths."""

    stock: Path = BootImagePaths.STOCK.value

    magisk: Path = BootImagePaths.MAGISK.value

    @property
    def path_list(self) -> list[Path]:
        """List of all boot image paths."""
        return [Path(enum_member.value) for enum_member in BootImagePaths]


# Signed off by Brian Sanford on 20260129
