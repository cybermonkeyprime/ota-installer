from dataclasses import dataclass, field
from typing import Any

import styles

import build.display.template as template


@dataclass
class Separator(template.DisplayComponent):
    indent: int = field(default=0)
    char: str = field(default="")

    def return_display(self) -> styles.Separator:
        return styles.Separator(self.indent, self.char)

    def display(self) -> Any:
        return self.return_display()
