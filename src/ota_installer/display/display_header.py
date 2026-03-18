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


@decorators.FooterWrapper(message="")
def show_display_header() -> None:
    """Renders the display header by invoking the components in sequence."""
    components = (
        DisplayHeader.TITLE.render_default,
        DisplayHeader.MOVE_CURSOR_UP.render_default,
        DisplayHeader.SEPARATOR.render_green,
        DisplayHeader.SUBTITLE.render_default,
    )
    for component in components:
        if not execute_component(component):
            logger.error("An error occurred during initialization.")


def execute_component(component) -> bool:
    """Executes a display component and returns success status."""
    return component() if component else False


def main():
    show_display_header()


if __name__ == "__main__":
    main()
