from dataclasses import dataclass, field
from typing import NamedTuple

import src.display.objects as display_object_types
import src.display.objects as display_objects
from src.decorators import Colorizer, FooterWrapper, OutputPrinter
from src.styles.escape_code_manager import EscapeCodeManager

DisplayObjectTypes = display_object_types.DisplayObjectTypes
DisplayObjectProcessor = display_objects.DisplayObjectProcessor


class DisplayFormatterTypes(NamedTuple):
    title: str
    major_number: int
    minor_number: int
    patch_number: int


@dataclass
class DisplayFormatter(object):
    title: str = field(default="Title")
    major_number: int = field(default=1)
    minor_number: int = field(default=1)
    patch_number: int = field(default=1)

    @FooterWrapper(message="")
    def __post_init__(self) -> None:
        try:
            self.header()
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    def header(self) -> bool:
        self.display_title()
        self.move_cursor_up()
        self.display_separator()
        self.display_versioning()
        return True

    @OutputPrinter(suffix="")
    def display_title(self) -> str:
        return self.process_display_object(DisplayObjectTypes.TITLE)

    @OutputPrinter(suffix="")
    def move_cursor_up(self) -> str:
        escape_code_manager = EscapeCodeManager()
        move_cursor_up = escape_code_manager.fetch_escape_code(
            "move_cursor_up"
        )
        return move_cursor_up

    @OutputPrinter(suffix="")
    @Colorizer(style="title")
    def display_separator(self) -> str:
        return self.process_display_object(DisplayObjectTypes.SEPARATOR)

    @OutputPrinter()
    def display_versioning(self) -> str:
        return self.process_display_object(DisplayObjectTypes.SUBTITLE)

    def process_display_object(self, _object: DisplayObjectTypes) -> str:
        return DisplayObjectTypes[_object.name].processor
