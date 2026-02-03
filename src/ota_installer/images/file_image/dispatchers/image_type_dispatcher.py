# src/ota_installer/images/file_image/dispatchers/image_type_dispatcher.py
from dataclasses import dataclass, field
from enum import Enum

from ....dispatchers.constants.dispatcher_constants import (
    DispatcherConstants,
)
from ....dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ....dispatchers.templates.dispatcher_template import DispatcherTemplate


class ImageType(Enum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"


@dispatcher_plugin(DispatcherConstants.IMAGE.value)
@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    """Dispatcher for handling image types."""

    obj: type = field(default_factory=lambda: type)

    @property
    def allowed_keys(self) -> tuple:
        """Returns a tuple of allowed image type keys."""
        return tuple(enum.name for enum in ImageType)

    def get_key(self, key: str) -> object:
        """Retrieves the value associated with the given key."""
        normalized_key = key.upper()
        evaluated_key = (
            normalized_key
            if normalized_key in self.allowed_keys
            else "DEFAULT"
        )
        return ImageType[evaluated_key].value
