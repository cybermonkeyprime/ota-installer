# src/ota_installer/images/file_image/constants/file_image_names.py
from enum import StrEnum, auto


class FileImageNames(StrEnum):
    PAYLOAD = auto()
    STOCK = auto()
    MAGISK = auto()


def main():
    print(FileImageNames.PAYLOAD.value)
    print(FileImageNames.STOCK.value)
    print(FileImageNames.MAGISK.value)


if __name__ == "__main__":
    main()
