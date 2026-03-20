# src/ota_installer/display/show_display_header.py
# from collections.abc import Callable
from collections.abc import Callable
from enum import StrEnum, auto

from rich.control import Control

from ... import decorators
from ...log_setup import logger
from ..components.separator import display_separator
from ..components.subtitle import display_subtitle
from ..components.title import display_title


class DisplayHeader(StrEnum):
    TITLE = auto()
    MOVE_CURSOR_UP = auto()
    SEPARATOR = auto()
    SUBTITLE = auto()

    @property
    def build(self) -> str:
        """Build the display content for this header component."""
        mapping: dict[DisplayHeader, Callable[[], str] | str] = {
            DisplayHeader.TITLE: display_title,
            DisplayHeader.MOVE_CURSOR_UP: str(Control.move(y=-1)),
            DisplayHeader.SEPARATOR: display_separator,
            DisplayHeader.SUBTITLE: display_subtitle,
        }

        value = mapping[self]

        if callable(value):
            return value()

        return value

    @decorators.OutputPrinter(suffix="")
    def render_default(self) -> str:
        """Render the component with default styling."""
        return self.build

    @decorators.OutputPrinter(suffix="")
    @decorators.Colorizer(style="title")
    def render_green(self) -> str:
        """Render the component with green title styling."""
        return self.build

    @classmethod
    def get_rendering_sequence(cls) -> tuple[Callable[[], bool], ...]:
        return (
            cls.TITLE.render_default,
            cls.MOVE_CURSOR_UP.render_default,
            cls.SEPARATOR.render_green,
            cls.SUBTITLE.render_default,
        )

    @classmethod
    @decorators.FooterWrapper(message="")
    def render_all(cls) -> None:
        """Render the display header by invoking the components in sequence."""
        for component in cls.get_rendering_sequence():
            if not cls.execute_component(component):
                logger.error("An error occurred during initialization.")

    @staticmethod
    def execute_component(component: Callable[[], bool] | None) -> bool:
        """Execute a display component and return success status."""
        return component() if component else False


def main() -> None:
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
