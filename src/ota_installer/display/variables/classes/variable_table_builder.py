# src/ota_installer.display/variables/classes/variable_table_builder.py
from dataclasses import dataclass

from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from ....styles.palette import RichColors


@dataclass
class VariableTableBuilder(object):
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


