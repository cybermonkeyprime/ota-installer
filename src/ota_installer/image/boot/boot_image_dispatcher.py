# src/ota_installer/image/boot/boot_image_dispatcher.py
from dataclasses import dataclass, field

from ...dispatcher.dispatcher_template import DispatcherTemplate
from ...dispatcher.dispatcher_type import DispatcherType
from ...plugin.plugin_registry import Plugin
from .boot_image_type import BootImageType


@Plugin.DISPATCHER.register(name=DispatcherType.IMAGE.value)
@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def get_key(self, key: str) -> str:
        """Normalizes the provided key and returns the corresponding image
        type value.
        """
        return BootImageType.validate_key(key)


# Signed off by Brian Sanford on 20260831
