# src/ota_installer/images/file_image/dispatchers/image_type_dispatcher.py
from dataclasses import dataclass, field
from enum import Enum

from ....dispatchers.constants.dispatcher_constants import (
    DispatcherConstants,
)
from ....dispatchers.dispatcher_plugin_registry import dispatcher_plugin
from ....dispatchers.templates.dispatcher_template import DispatcherTemplate


class ImageTypes(Enum):
    TOKAY = "init_boot"
    SHIBA = "init_boot"
    DEFAULT = "init_boot"


@dispatcher_plugin(DispatcherConstants.IMAGE.value)
@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    @property
    def allowed_keys(self) -> tuple:
        return tuple(enum.name for enum in ImageTypes)

    def get_key(self, key: str) -> object:
        key_to_upper = key.upper()
        evaluated_key = (
            "DEFAULT"
            if key_to_upper not in self.allowed_keys
            else key_to_upper
        )
        key_object = ImageTypes[evaluated_key]
        return key_object.value
