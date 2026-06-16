# display/variable/variable_item_handler.py
from dataclasses import dataclass

from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from ...style.style_info import RichColors
from ...variable.variable_manager import VariableManager


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


# Directory names


def set_ota_file_directory(
    processing_function: VariableManager,
) -> None:
    """Sets the OTA file directory in the processing function."""

    from ..variable.processor.file_process_info import VariableFileProcessor

    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_directory")
        .set_value("path.parent")
        .process_items()
    )


def set_magisk_image_directories(
    processing_function: VariableManager,
) -> None:
    """Sets the Magisk image directories in the processing function."""

    from ..variable.processor.directory_process_info import (
        DirectoryIterationProcessor,
    )

    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("local", "remote"))
        .set_directory_type("magisk")
        .set_variable_prefix("_")
        .process_items()
    )


def set_boot_image_directories(
    processing_function: VariableManager,
) -> None:
    """Sets the boot image directories in the processing function."""

    from ..variable.processor.directory_process_info import (
        DirectoryIterationProcessor,
    )

    (
        DirectoryIterationProcessor(processing_function)
        .set_directory_names(("stock", "magisk"))
        .set_directory_type("")
        .set_variable_prefix("")
        .process_items()
    )


# File names


def set_ota_file_name(processing_function: VariableManager) -> None:
    """Sets the OTA file name in the processing function."""

    from ..variable.processor.file_process_info import VariableFileProcessor

    (
        VariableFileProcessor(processing_function)
        .set_title("ota_file_name")
        .set_value("path.name")
        .process_items()
    )


def set_image_file_names(
    processing_function: VariableManager,
) -> None:
    """Sets the image file names in the processing function."""

    from ..variable.processor.file_process_info import (
        FileIterationProcessor,
    )

    (
        FileIterationProcessor(processing_function)
        .set_file_names(("payload", "stock", "magisk"))
        .process_items()
    )


def set_log_file(processing_function: VariableManager) -> None:
    """Sets the log file in the processing function."""

    from ..variable.processor.file_process_info import VariableFileProcessor

    (
        VariableFileProcessor(processing_function)
        .set_title("log_file")
        .set_value("log_file")
        .process_items()
    )


# Signed off by Brian Sanford on 20260510
