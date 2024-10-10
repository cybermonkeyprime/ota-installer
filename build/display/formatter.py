from dataclasses import dataclass, field
from typing import Any

from ..decorators import Colorizer, FooterWrapper, Printer

from ..styles.escape_code_manager import EscapeCodeManager

import build.display.components as display_components


@dataclass
class Formatter:
    title: str = field(default="Title")
    build: int = field(default=1)
    revision: int = field(default=1)

    @FooterWrapper(message="")
    def __post_init__(self) -> None:
        try:
            self.display_title()
            self.move_cursor_up()
            self.display_separator()
            self.display_subtitle()
        except Exception as e:
            Printer(f"An error occurred during initialization: {e}")

    @Printer(suffix="")
    def display_title(self) -> Any:
        component = display_components.Title(self.title)
        return component.display()

    @Printer(suffix="")
    def move_cursor_up(self) -> str:
        escape_code_manager = EscapeCodeManager()
        move_cursor_up = escape_code_manager.fetch_escape_code("move_cursor_up")
        return move_cursor_up

    @Printer(suffix="")
    @Colorizer(style="title")
    def display_separator(self, indent: int = 9, char: str = "-") -> str:
        component = display_components.Separator(indent, char[0])
        return f"{component.display()}> "

    @Printer()
    def display_subtitle(self) -> str:
        component = display_components.Subtitle(self.build, self.revision)
        return component.display()
