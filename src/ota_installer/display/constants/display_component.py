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

        if self not in self._mapping:
            raise NotImplementedError(
                f"LOUD FAIL: '{self.name}' is defined in DisplayComponent "
                f"but missing from the _mapping dictionary."
            )

        return self._mapping[self]()


# Signed off by Brian Sanford on 20260310
