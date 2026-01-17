# src/ota_installer/images/boot_image/dispatchers/boot_image_dispatcher.py
from dataclasses import dataclass, field
from enum import Enum

from ....dispatchers.templates.dispatcher_template import DispatcherTemplate


class ImageTypes(Enum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"


@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    @property
    def allowed_keys(self) -> tuple:
        """Returns a tuple of allowed image type keys in lowercase."""
        return tuple(enum.name.lower() for enum in ImageTypes)

    def get_key(self, key: str) -> object:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        normalized_key = self.normalize_key(key)
        evaluated_key = (
            "DEFAULT"
            if normalized_key not in self.allowed_keys
            else normalized_key
        )
        key_object = ImageTypes[evaluated_key]
        return key_object.value


# Signed off by Brian Sanford on 20260116
