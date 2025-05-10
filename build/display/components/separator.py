from dataclasses import dataclass, field
from typing import Any

import styles

from build.display.display_template import DisplayComponent


@dataclass
class Separator(DisplayComponent):
    indent: int = field(default=0)
    char: str = field(default="")

    def return_display(self) -> styles.Separator:
        return styles.Separator(self.indent, self.char)

    def get_display(self) -> Any:
        return self.return_display()


@dataclass
class DisplaySeparator(object):
    indent: int = field(default=9)
    char: str = field(default="-")

    # @property
    # def component(self) -> Separator:
    #    return Separator(self.indent, self.char[0])

    def __str__(self) -> str:
        component = Separator(self.indent, self.char[0])
        return f"{component.get_display()}> "
