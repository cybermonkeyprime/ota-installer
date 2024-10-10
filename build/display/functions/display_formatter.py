from dataclasses import dataclass, field
from typing import Any

from build.decorators import Colorizer, FooterWrapper, Printer

from .components import DisplaySubtitle, DisplayTitle, Separator


@dataclass
class DisplayFormatter:
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
        component = DisplayTitle(self.title)
        return component.display()

    @Printer(suffix="")
    def move_cursor_up(self) -> str:
        return "\033[F"

    @Printer(suffix="")
    @Colorizer(style="title")
    def display_separator(self, indent: int = 9, char: str = "-") -> str:
        component = Separator(indent, char[0])
        return f"{component.display()}> "
        # return str(component.display())

    @Printer()
    def display_subtitle(self) -> str:
        component = DisplaySubtitle(self.build, self.revision)
        return component.display()
