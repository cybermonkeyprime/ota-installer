# display/variable/variable_item_handler.py
from dataclasses import dataclass

from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from ...style.style_info import RichColors


@dataclass(frozen=True, slots=True)
class VariableItemContainer:
    """Represents a variable item with a title and a value."""

    title: str
    value: str


@dataclass
class VariableTableBuilder:
    """Builds a table for displaying variable titles and their values."""

    def __init__(self, indent: int = 3) -> None:
        """Initializes the table with columns for titles and values."""
        self.table = Table(title="", show_header=False, box=None)
        self.table.add_column(
            "Title",
            no_wrap=True,
            justify="left",
            style=RichColors.VARIABLE.value,
        )
        self.table.add_column(
            "Value", justify="left", style=RichColors.VARIABLE.value
        )
        self.indent = indent

    def add(self, title: str, value: str) -> None:
        """Adds a row to the table with a title and its corresponding value."""
        self.table.add_row(f"{title.upper()}:", value)

    def newline(self) -> None:
        """Adds an empty row to the table for spacing."""
        self.table.add_row("", "")

    def render(self) -> None:
        """Renders the table to the console with specified indentation."""
        console = Console()
        console.print(Padding(self.table, (0, 0, 0, self.indent)))


# Signed off by Brian Sanford on 20260510
