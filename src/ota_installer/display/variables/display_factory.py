# src/ota_installer/display/factories/display_factory.py
from rich.control import Control

from ... import decorators
from ...log_setup import logger
from ..constants.display_component_calls import DisplayComponentCalls


@decorators.FooterWrapper(message="")
def create_display_objects() -> None:
    """Creates and displays the display objects."""
    try:
        display_header()
    except Exception as err:
        logger.error(
            f"format_display(): An error occurred during initialization: {err}"
        )


def display_header() -> bool:
    """Displays the header section of the display."""
    show_title()
    move_cursor_up()
    show_separator()
    show_subtitle()
    return True


@decorators.OutputPrinter(suffix="")
def show_title() -> str:
    """Displays the title."""
    return DisplayComponentCalls.title.processor


@decorators.OutputPrinter(suffix="")
def move_cursor_up() -> str:
    """Moves the cursor up by one line."""
    return str(Control.move(y=-1))


@decorators.OutputPrinter(suffix="")
@decorators.Colorizer(style="title")
def show_separator() -> str:
    """Displays a separator line."""
    return DisplayComponentCalls.separator.processor


@decorators.OutputPrinter()
def show_subtitle() -> str:
    """Displays the subtitle."""
    return DisplayComponentCalls.subtitle.processor


def main():
    """Main entry point for the display creation."""
    create_display_objects()


if __name__ == "__main__":
    main()
