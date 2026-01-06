# src/ota_installer/display/factories/display_factory.py
from rich.control import Control

from .. import decorators
from ..log_setup import logger
from .objects.constants.display_object_function_calls import (
    DisplayObjectFunctionCalls,
)


@decorators.FooterWrapper(message="")
def show_display_components() -> None:
    try:
        display_header()
    except Exception as err:
        logger.error(
            f"format_display(): An error occurred during initialization: {err}"
        )


def display_header() -> bool:
    show_title()
    move_cursor_up()
    show_separator()
    show_subtitle()
    return True


@decorators.OutputPrinter(suffix="")
def show_title() -> str:
    return DisplayObjectFunctionCalls.TITLE.processor


@decorators.OutputPrinter(suffix="")
def move_cursor_up() -> str:
    return str(Control.move(y=-1))


@decorators.OutputPrinter(suffix="")
@decorators.Colorizer(style="title")
def show_separator() -> str:
    return DisplayObjectFunctionCalls.SEPARATOR.processor


@decorators.OutputPrinter()
def show_subtitle() -> str:
    return DisplayObjectFunctionCalls.SUBTITLE.processor


def main():
    show_display_components()


if __name__ == "__main__":
    main()
