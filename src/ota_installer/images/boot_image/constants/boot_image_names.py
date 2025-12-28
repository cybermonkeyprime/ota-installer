# src/ota_installer/images/boot_image/constants/boot_image_names.py
from enum import StrEnum, auto


class BootImageNames(StrEnum):
    PAYLOAD = auto()
    STOCK = auto()
    MAGISK = auto()


def main():
    print(BootImageNames.PAYLOAD.value)
    print(BootImageNames.STOCK.value)
    print(BootImageNames.MAGISK.value)


if __name__ == "__main__":
    main()
