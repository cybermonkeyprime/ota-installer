# src/ota_installer/boot_image/constants/paths.py
from enum import Enum
from pathlib import Path


class BootImagePaths(Enum):
    PAYLOAD = Path.home()
    STOCK = Path.home() / "Android" / "boot-images" / "stock"
    MAGISK = Path.home() / "Android" / "boot-images" / "magisk"


def main():
    print(BootImagePaths.PAYLOAD.value)
    print(BootImagePaths.STOCK.value)
    print(BootImagePaths.MAGISK.value)


if __name__ == "__main__":
    main()
