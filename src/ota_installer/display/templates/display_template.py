# src/ota_installer/display/templates/display_template.py
from typing import Protocol


class DisplayComponent(Protocol):
    """Interface for display components that provide a display string.

    This interface defines a method to retrieve the display string
    for a component.
    """

    def get_display(self) -> str:
        """Return the display string for the component."""
        raise NotImplementedError()


