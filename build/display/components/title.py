from dataclasses import dataclass, field

from build.decorators import ColorizedFiglet
from build.display.display_template import DisplayComponent


@dataclass
class Title(DisplayComponent):
    title: str = field(default="ota-installer")

    @ColorizedFiglet(style="title", font="slant")
    def return_display(self) -> str:
        return f" {self.title}"

    def display(self) -> str:
        return self.return_display()
