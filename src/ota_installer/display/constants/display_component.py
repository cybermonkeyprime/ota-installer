# src/ota_installer/display/components/constants/display_component.py
from enum import Enum, auto


class DisplayComponent(Enum):
    """
    Classifies different types of components that can be used in a display.
    """

    TITLE = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()
