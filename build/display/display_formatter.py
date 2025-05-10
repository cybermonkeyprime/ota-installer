from dataclasses import dataclass, field

import build.display.components as dc
from build.decorators import Colorizer, FooterWrapper, Printer
from build.display.display_objects import (
    DisplayObjectTemplate,
    DisplayObjectAttributes,
    DisplayObjectProcessor,
)
from build.styles.escape_code_manager import EscapeCodeManager


@dataclass
class DisplayFormatter(object):
    title: str = field(default="OTA-Installer")
    major_number: int = field(default=1)
    minor_number: int = field(default=1)
    patch_number: int = field(default=1)

    @FooterWrapper(message="")
    def __post_init__(self) -> None:
        try:
            self.header()
        except Exception as e:
            Printer(f"An error occurred during initialization: {e}")

    def header(self) -> bool:
        self.display_title()
        self.move_cursor_up()
        self.display_separator()
        self.display_versioning()
        return True

    @Printer(suffix="")
    def display_title(self) -> "DisplayObjectAttributes":
        return self.process_display_object("display_title")

    @Printer(suffix="")
    def move_cursor_up(self) -> str:
        escape_code_manager = EscapeCodeManager()
        move_cursor_up = escape_code_manager.fetch_escape_code(
            "move_cursor_up"
        )
        return move_cursor_up

    @Printer(suffix="")
    @Colorizer(style="title")
    def display_separator(self) -> "DisplayObjectAttributes":
        return self.process_display_object("display_separator")

    @Printer()
    def display_versioning(self) -> "DisplayObjectAttributes":
        return self.process_display_object("display_versioning")

    #    @Printer()
    def process_display_object(
        self, object_title: str
    ) -> DisplayObjectAttributes:
        display_object_processor = DisplayObjectProcessor(object_title)
        return display_object_processor.process_object()
