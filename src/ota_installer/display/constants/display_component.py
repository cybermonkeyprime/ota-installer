# src/ota_installer/display/components/constants/display_component.py
from collections.abc import Callable
from enum import StrEnum, auto

from ..components.separator import display_separator
from ..components.subtitle import display_subtitle
from ..components.title import display_title


class DisplayComponent(StrEnum):
    """Enumerates the various components used in a display."""

    TITLE = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @property
    def _mapping(self) -> dict["DisplayComponent", Callable[[], str]]:
        """Internal mapping of enum members to functions."""
        return {
            DisplayComponent.TITLE: display_title,
            DisplayComponent.SEPARATOR: display_separator,
            DisplayComponent.SUBTITLE: display_subtitle,
        }

    @property
    def render(self) -> str:
        """Triggers the associated display function."""

        display_function = self._mapping.get(self)
        if not display_function:
            raise ValueError(f"No display function defined for: {self.value}")

        return display_function()


# Signed off by Brian Sanford on 20260310
