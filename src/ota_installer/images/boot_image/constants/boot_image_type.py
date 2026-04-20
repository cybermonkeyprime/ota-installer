# src/ota_installer/images/boot_image/constants/boot_image_type.py
from enum import StrEnum


class BootImageType(StrEnum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"

    @classmethod
    def allowed_types(cls) -> tuple:
        """Returns a tuple of allowed image type keys in lowercase."""
        return tuple(enum.name.lower() for enum in cls)

    @staticmethod
    def normalize_key(key: str) -> str:
        """Normalize dictionary keys for consistent dispatcher behavior."""
        return key.lower().strip()

    @classmethod
    def get_key(cls, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        normalized_key = cls.normalize_key(key)
        return cls[normalized_key.upper()] or cls.DEFAULT.value
