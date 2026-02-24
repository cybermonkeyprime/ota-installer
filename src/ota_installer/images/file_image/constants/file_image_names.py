# src/ota_installer/images/file_image/constants/file_image_names.py
from enum import StrEnum, auto


class FileImageNames(StrEnum):
    """Enumeration for File Image Names."""

    STOCK = auto()
    PAYLOAD = auto()
    MAGISK = auto()

    @classmethod
    def create_path_dictionary(cls, file_paths) -> dict:
        """create the dictionary with enum member names and their
        corresponding values.
        """
        return {
            cls.normalize_key(enum_member): getattr(
                file_paths, enum_member.value
            )
            for enum_member in cls
        }

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.strip()


def print_image_names():
    """Prints the values of FileImageNames enum."""
    for image_name in FileImageNames:
        print(image_name.value)


def main():
    """Main function that prints file image names."""
    print_image_names()


if __name__ == "__main__":
    pass

# Signed off by Brian Sanford on 20260203
