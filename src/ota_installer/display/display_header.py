# src/ota_installer/display/show_display_header.py
from rich.control import Control

from .. import decorators
from ..log_setup import logger
from .constants.display_component import DisplayComponent
from .constants.display_component_calls import (
    call_display_component,
)


@decorators.FooterWrapper(message="")
def show_display_header() -> None:
    """Renders the display header by invoking the components in sequence."""
    components = (show_title, move_cursor_up, show_separator, show_subtitle)
    for component in components:
        try:
            component()
        except Exception as err:
            logger.error(
                "format_display(): An error occurred during initialization: "
                f"{err}"
            )


@decorators.OutputPrinter(suffix="")
def show_title() -> str:
    """Returns the title for the display."""
    return call_display_component(DisplayComponent.TITLE)


@decorators.OutputPrinter(suffix="")
def move_cursor_up() -> str:
    """Returns the control sequence to move the cursor up in the console."""
    return str(Control.move(y=-1))


@decorators.OutputPrinter(suffix="")
@decorators.Colorizer(style="title")
def show_separator() -> str:
    """Returns the separator for the display."""
    return call_display_component(DisplayComponent.SEPARATOR)


@decorators.OutputPrinter()
def show_subtitle() -> str:
    """Returns the subtitle for the display."""
    return call_display_component(DisplayComponent.SUBTITLE)


def main():
    show_display_header()


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260213
