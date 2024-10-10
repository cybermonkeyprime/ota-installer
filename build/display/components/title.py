from dataclasses import dataclass, field

import build.display.template as template
from build.decorators import ColorizedFiglet


@dataclass
class Title(template.DisplayComponent):
    title: str = field(default="ota-installer")

    @ColorizedFiglet(style="title", font="slant")
    def return_display(self) -> str:
        return f" {self.title}"

    def display(self) -> str:
        return self.return_display()
