from dataclasses import dataclass, field
from pathlib import Path

from build.decorators import ColorizedIndentPrinter


@dataclass
class OutputFormatter(object):
    """Formats and prints variable output."""

    title: str = field(default="")
    value: type | Path | None = field(default=None)

    @ColorizedIndentPrinter(indent=1)
    def format_and_print(self) -> str:
        return f"{self.title.upper()}: {self.value}"
