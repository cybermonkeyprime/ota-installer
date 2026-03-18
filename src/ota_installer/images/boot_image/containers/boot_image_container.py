# src/ota_installer/images/boot_image/containers/boot_image_conatiner.py
from dataclasses import dataclass
from pathlib import Path

from ..constants.boot_image_paths import BootImagePaths


@dataclass(frozen=True, slots=True)
class BootImageContainer(object):
    """Container for boot image paths."""

    stock: Path = BootImagePaths.STOCK.value

    magisk: Path = BootImagePaths.MAGISK.value


# Signed off by Brian Sanford on 20260318
