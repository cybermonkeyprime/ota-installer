# src/ota_installer/display/show_display_header.py
from enum import StrEnum

from rich.control import Control

from .. import decorators
from ..log_setup import logger
from .constants.display_component import DisplayComponent


class DisplayHeader(StrEnum):
    TITLE = DisplayComponent.TITLE.render
    MOVE_CURSOR_UP = str(Control.move(y=-1))
    SEPARATOR = DisplayComponent.SEPARATOR.render
    SUBTITLE = DisplayComponent.SUBTITLE.render

    @decorators.OutputPrinter(suffix="")
    def render_default(self) -> str:
        """Returns the component for the display."""
        return self.value

    @decorators.OutputPrinter(suffix="")
    @decorators.Colorizer(style="title")
    def render_green(self) -> str:
        """Returns the component for the display in green."""
        return self.value

    @classmethod
    def get_rendering_sequence(cls) -> tuple:
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
        for component in DisplayHeader.get_rendering_sequence():
            if not cls.execute_component(component):
                logger.error("An error occurred during initialization.")

    @staticmethod
    def execute_component(component) -> bool:
        """Executes a display component and returns success status."""
        return component() if component else False


def main():
    DisplayHeader.render_all()


if __name__ == "__main__":
    main()
