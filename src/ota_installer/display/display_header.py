# src/ota_installer/display/show_display_header.py
from rich.control import Control

from .. import decorators
from ..log_setup import logger
from .constants.display_component import DisplayComponent
from .constants.display_component_calls import (
    display_component_calls,
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
                f"format_display(): An error occurred during initialization: "
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


def call_display_component(
    component_type: DisplayComponent, *args, **kwargs
) -> str:
    """Call the display function associated with the given component type."""
    display_function = display_component_calls[component_type]
    if not display_function:
        raise ValueError(
            f"Display component {component_type} is not registered."
        )
    return display_function(*args, **kwargs)


def main():
    show_display_header()


if __name__ == "__main__":
    main()
