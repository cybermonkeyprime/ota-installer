# src/ota_installer/display/constants/display_component_calls.py
from collections.abc import Callable
from enum import Enum

from ..components.separator import display_separator
from ..components.subtitle import display_subtitle
from ..components.title import display_title


class DisplayCall(Enum):
    TITLE = (display_title,)
    SEPARATOR = (display_separator,)
    SUBTITLE = (display_subtitle,)

    def __init__(self, display_function: Callable) -> None:
        self.display_function = display_function

    @property
    def render(self) -> str:
        if not self.display_function:
            raise ValueError(
                f"Display component {self.name.lower()} is not registered."
            )
        return self.display_function()
