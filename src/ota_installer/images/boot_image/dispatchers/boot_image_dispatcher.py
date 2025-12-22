# src/ota_installer/images/boot_image/dispatchers/boot_image_dispatcher.py
from dataclasses import dataclass, field
from enum import Enum

from ....dispatchers.templates import DispatcherTemplate


class ImageTypes(Enum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"


@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    @property
    def allowed_keys(self) -> tuple:
        return tuple(enum.name for enum in ImageTypes)

    def get_key(self, key: str) -> object:
        key_to_upper = key.upper()
        evaluated_key = (
            key_to_upper if key_to_upper in self.allowed_keys else "DEFAULT"
        )
        key_object = ImageTypes[evaluated_key]
        return key_object.value
