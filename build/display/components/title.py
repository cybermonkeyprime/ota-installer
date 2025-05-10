from dataclasses import dataclass, field

from build.decorators import ColorizedFiglet
from build.display.display_template import DisplayComponent


@dataclass
class Title(DisplayComponent):
    title: str = field(default="ota-installer")

    @ColorizedFiglet(style="title", font="slant")
    def return_display(self) -> str:
        return f" {self.title}"

    def get_display(self) -> str:
        return self.return_display()


@dataclass
class DisplayTitle(object):
    title: str = field(default_factory=str)

    def __str__(self) -> str:
        component = Title(self.title)
        return component.get_display()
