# src/ota_installer/images/file_image/constants/file_image_names.py
from enum import StrEnum, auto


class FileImageNames(StrEnum):
    """Enumeration for File Image Names."""

    STOCK = auto()
    PAYLOAD = auto()
    MAGISK = auto()


def print_image_names():
    """Prints the values of FileImageNames enum."""
    for image_name in FileImageNames:
        print(image_name.value)


def main():
    """Main function that prints file image names."""
    print_image_names()


if __name__ == "__main__":
    pass
