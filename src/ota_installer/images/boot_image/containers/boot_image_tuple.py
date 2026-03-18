# src/ota_installer/images/boot_image/containers/boot_image_tuple.py
from pathlib import Path
from typing import NamedTuple


class BootImageTuple(NamedTuple):
    """Represents a boot image with stock and magisk paths."""

    stock: Path
    magisk: Path

    def is_valid(self) -> bool:
        """Checks if both stock and magisk paths are valid."""
        return self.stock.exists() and self.magisk.exists()


