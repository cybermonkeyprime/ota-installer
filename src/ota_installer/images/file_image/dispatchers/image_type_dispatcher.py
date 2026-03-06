# src/ota_installer/images/file_image/dispatchers/image_type_dispatcher.py
from dataclasses import dataclass, field
from enum import Enum

from ....dispatchers.constants.dispatcher_constants import (
    DispatcherConstants,
)
from ....dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ....dispatchers.templates.dispatcher_template import DispatcherTemplate


class ImageType(Enum):
    """Enumeration of supported image types."""

    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"

    @classmethod
    def allowed_keys(cls) -> tuple:
        """Returns a tuple of allowed image type keys."""
        return tuple(cls.__members__.keys())


@dispatcher_plugin(DispatcherConstants.IMAGE.value)
@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling image types."""

    obj: type = field(default_factory=lambda: type)

    def get_key(self, key: str) -> str:
        """Retrieves the value associated with the given key."""
        return getattr(ImageType, key.upper(), ImageType.DEFAULT).value


# Signed off by Brian Sanford on 20260305
