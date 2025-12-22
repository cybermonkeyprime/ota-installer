# src/ota_installer/display/objects/containers/display_object_container.py
from typing import NamedTuple


# Type alias for better readability
class DisplayObjectContainer(NamedTuple):
    """
    NamedTuple to represent a display object with its associated metadata.
    """

    object_name: str
    class_name: type
    class_argument: str | None
