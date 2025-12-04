# src/display/objects/types/display_object_types.py
from dataclasses import dataclass, field
from enum import Enum
from typing import NamedTuple

import src.display.components as dc


# Enums for better readability and maintainability
class DisplayObjectTypes(Enum):
    TITLE = "title"
    SEPARATOR = "separator"
    SUBTITLE = "subtitle"

    @property
    def display_objects(self) -> "DisplayObjectDictionary":
        return DisplayObjectDictionary()

    @property
    def get_dict_item(self) -> object:
        return self.display_objects.display_objects[self.name]

    def __str__(self) -> str:
        return self.value


# Type alias for better readability
DisplayObjectDictionaryTypes = dict[
    DisplayObjectTypes | str, "DisplayObjectAttributes"
]


@dataclass
class DisplayObjectAttributes(NamedTuple):
    object_type: type
    argument: str | None


@dataclass
class DisplayObjectDictionary(object):
    display_title: str = field(default="OTA-Installer")

    @property
    def display_objects(self) -> DisplayObjectDictionaryTypes:
        return {
            DisplayObjectTypes.TITLE: DisplayObjectAttributes(
                dc.DisplayTitle, self.display_title
            ),
            DisplayObjectTypes.SEPARATOR: DisplayObjectAttributes(
                dc.DisplaySeparator, None
            ),
            DisplayObjectTypes.SUBTITLE: DisplayObjectAttributes(
                dc.DisplaySubtitle, None
            ),
        }
