from dataclasses import dataclass, field

from decorators import Colorizer

import build.display.template as template


@dataclass
class Subtitle(template.DisplayComponent):
    build: int = field(default=0)
    revision: int = field(default=0)

    def display(self) -> str:
        build_str = self.build_formatter()
        revision_str = self.revision_formatter()
        return f"{build_str} {revision_str}"

    @Colorizer(style="version")
    def build_formatter(self) -> str:
        return f"Build: {self.build}"

    @Colorizer(style="version")
    def revision_formatter(self) -> str:
        if self.revision > 0:
            return f"\b (Rev: {self.revision})"
        else:
            return "\b"  # backspace
