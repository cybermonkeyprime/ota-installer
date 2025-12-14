from dataclasses import dataclass, field

from rich.control import Control

from src.decorators import Colorizer, FooterWrapper, OutputPrinter

from ..components import DisplaySubtitle, DisplayTitle, Separator


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
            # self.display_separator()
            self.display_subtitle()
        except Exception as e:
            print(f"An error occurred during initialization: {e}")

    @OutputPrinter(suffix="")
    def display_title(self) -> str:
        component = DisplayTitle(self.title)
        return component.get_display()

    @OutputPrinter(suffix="")
    def move_cursor_up(self) -> Control:
        control = Control()
        control.move(y=-1)
        return control  # control

    @OutputPrinter(suffix="")
    @Colorizer(style="title")
    def display_separator(self, indent: int = 9, char: str = "-") -> str:
        component = Separator(indent, char[0])
        return f"{component.get_display()}> "
        # return str(component.display())

    @OutputPrinter()
    def display_subtitle(self) -> str:
        component = DisplaySubtitle(self.build, self.revision)
        return component.get_display()
