# src/ota_installer/images/boot_image/constants/boot_image_paths.py
from enum import Enum
from pathlib import Path


class BootImagePaths(Enum):
    """Enumeration for boot image paths."""

    PAYLOAD = Path.home()
    STOCK = Path.home() / "Android" / "boot-images" / "stock"
    MAGISK = Path.home() / "Android" / "boot-images" / "magisk"

    @classmethod
    def path_list(cls) -> tuple[Path, ...]:
        """List of all boot image paths."""
        return tuple(Path(enum_member.value) for enum_member in cls)


def display_boot_image_paths() -> None:
    """Prints the paths for boot images."""
    for path in BootImagePaths.path_list():
        print(path)


if __name__ == "__main__":
    display_boot_image_paths()

# Signed off by Brian Sanford on 20260318
