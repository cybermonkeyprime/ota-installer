from dataclasses import dataclass, field

from build.decorators import Colorizer, FooterWrapper, Printer
from build.display.display_objects import DisplayObjectProcessor
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
    def display_title(self) -> "type":
        return self.process_display_object("display_title")

    @Printer(suffix="")
    def move_cursor_up(self) -> "CursorAdjustor":
        return CursorAdjustor("move_cursor_up")

    @Printer(suffix="")
    @Colorizer(style="title")
    def display_separator(self) -> "type":
        return self.process_display_object("display_separator")

    @Printer()
    def display_versioning(self) -> "type":
        return self.process_display_object("display_versioning")

    def process_display_object(self, obj_name: str) -> "type":
        display_object_processor = DisplayObjectProcessor(obj_name)
        return display_object_processor.process_object()


@dataclass()
class CursorAdjustor(object):
    position: str

    def __str__(self) -> str:
        escape_code_manager = EscapeCodeManager()
        return escape_code_manager.fetch_escape_code(self.position)

    pass
