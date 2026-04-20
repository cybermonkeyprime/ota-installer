# src/ota_installer/images/boot_image/dispatchers/boot_image_dispatcher.py
from dataclasses import dataclass, field

from ....dispatchers.templates.dispatcher_template import DispatcherTemplate
from ..constants.boot_image_type import BootImageType


@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def get_key(self, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        return BootImageType.get_key(key)


def retrieve_image_type_from_key(enum: type, key: str) -> str:
    return enum.get_key(key)


# Signed off by Brian Sanford on 20260317
