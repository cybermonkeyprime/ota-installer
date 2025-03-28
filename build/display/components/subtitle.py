from dataclasses import dataclass, field

from build.decorators import Colorizer

import build.display.template as template


@dataclass
class Subtitle(template.DisplayComponent):
    build: int = field(default=0)
    revision: int = field(default=0)

    @Colorizer(style="version")
    def display(self) -> str:
        return f"{self.build_string} {self.revision_string}"

    @property
    def build_string(self) -> str:
        return f"Build: {self.build}"

    @property
    def revision_string(self) -> str:
        return f"\b (Rev: {self.revision})" if self.revision > 0 else "\b"  # backspace
