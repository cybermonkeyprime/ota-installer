# src/ota_installer/images/boot_image/constants/boot_image_type.py
from enum import StrEnum


class BootImageType(StrEnum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"

    @classmethod
    def allowed_types(cls) -> tuple:
        """Returns a tuple of allowed image type keys in lowercase."""
        return tuple(key.lower() for key in cls.__members__.keys())

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()

    @classmethod
    def validate_key(cls, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        normalized_key = cls.normalize_key(key)
        return getattr(cls, normalized_key, cls.DEFAULT)


# Signed off by Brian Sanford on 20260420
