# src/ota_installer/display/formatters/display_formatter.py
from dataclasses import dataclass, field

from rich.control import Control

from ...decorators import (
    Colorizer,
    FooterWrapper,
    OutputPrinter,
)
from ..objects.constants.display_object_constants import DisplayObjectConstants


@dataclass
class DisplayFormatter(object):
    title: str = field(default="Title")
    major_number: int = field(default=0)
    minor_number: int = field(default=0)
    patch_number: int = field(default=0)

    @FooterWrapper(message="")
    def __post_init__(self) -> None:
        try:
            self.header()
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    def header(self) -> bool:
        self.show_title()
        self.move_cursor_up()
        self.show_separator()
        self.show_subtitle()
        return True

    @OutputPrinter(suffix="")
    def show_title(self) -> str:
        return self.process_display_object(DisplayObjectConstants.TITLE)

    @OutputPrinter(suffix="")
    def move_cursor_up(self) -> str:
        return str(Control.move(y=-1))

    @OutputPrinter(suffix="")
    @Colorizer(style="title")
    def show_separator(self) -> str:
        return self.process_display_object(DisplayObjectConstants.SEPARATOR)

    @OutputPrinter()
    def show_subtitle(self) -> str:
        return self.process_display_object(DisplayObjectConstants.SUBTITLE)

    def process_display_object(self, _object: DisplayObjectConstants) -> str:
        return DisplayObjectConstants[_object.name].processor
