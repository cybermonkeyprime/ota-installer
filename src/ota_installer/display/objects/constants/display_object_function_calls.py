# src/ota_installer/display/objects/constants/display_object_functions.py
from enum import Enum

from ...components.separator import display_separator
from ...components.subtitle import display_subtitle
from ...components.title import display_title
from ..containers.display_object_container import DisplayObjectContainer


# Enums for better readability and maintainability
class DisplayObjectFunctionCalls(Enum):
    """Enum representing different types of display objects."""

    TITLE = DisplayObjectContainer("title", display_title)
    SEPARATOR = DisplayObjectContainer("separator", display_separator)
    SUBTITLE = DisplayObjectContainer("subtitle", display_subtitle)

    def __str__(self) -> str:
        """String representation of the DisplayObjectTypes enum."""

        return self.value.object_name

    @property
    def processor(self):
        """Property to process the associated display object."""

        return self.value.function()
