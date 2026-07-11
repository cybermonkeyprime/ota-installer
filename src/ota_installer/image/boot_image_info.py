# src/ota_installer/image/boot_image_info.py
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Self

from ..dispatcher.dispatcher_info import DispatcherTemplate, DispatcherType
from ..plugin.plugin_registry import dispatcher_plugin
from .generic_image_info import FileImageName


@dataclass(frozen=True, slots=True)
class BootImageContainer:
    """Container for boot image paths."""

    stock: Path

    magisk: Path

    @classmethod
    def create(cls) -> Self:
        return cls(**FileImageName.boot_directories())


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


@dispatcher_plugin(DispatcherType.IMAGE.value)
@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def get_key(self, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        return BootImageType.validate_key(key)
