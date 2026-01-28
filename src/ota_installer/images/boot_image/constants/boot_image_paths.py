# src/ota_installer/images/boot_image/constants/boot_image_paths.py
from enum import Enum
from pathlib import Path


class BootImagePaths(Enum):
    """Enumeration for boot image paths."""

    PAYLOAD = Path.home()
    STOCK = Path.home() / "Android" / "boot-images" / "stock"
    MAGISK = Path.home() / "Android" / "boot-images" / "magisk"


def display_boot_image_paths() -> None:
    """Prints the paths for boot images."""
    print(BootImagePaths.PAYLOAD.value)
    print(BootImagePaths.STOCK.value)
    print(BootImagePaths.MAGISK.value)


if __name__ == "__main__":
    display_boot_image_paths()
