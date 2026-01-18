# src/ota_installer/images/boot_image/containers/boot_image_tuple.py
from pathlib import Path
from typing import NamedTuple


class BootImageTuple(NamedTuple):
    """Represents a boot image with stock and magisk paths."""

    stock: Path
    magisk: Path


# Signed off by Brian Sanford on 20260118
