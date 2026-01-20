# src/ota_installer/display/components/constants/display_component.py
from enum import StrEnum, auto


class DisplayComponent(StrEnum):
    """
    Classifies different types of components that can be used in a display.
    """

    TITLE = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()


# Signed off by Brian Sanford on 20260108
