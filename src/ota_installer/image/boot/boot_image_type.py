# src/ota_installer/image/boot/boot_image_type.py
from enum import StrEnum


class BootImageType(StrEnum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"

    @classmethod
    def allowed_types(cls) -> tuple:
        """Returns a tuple of allowed image type keys in lowercase."""
        return tuple(key.lower() for key in cls.__members__)

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()

    @classmethod
    def validate_key(cls, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        normalized_key = cls.normalize_key(key).upper()
        return cls.__members__.get(normalized_key, cls.DEFAULT).value


# Signed off by Brian Sanford on 20260831
