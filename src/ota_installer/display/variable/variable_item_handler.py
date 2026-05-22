# display/variable/variable_item_handler.py
from dataclasses import dataclass, field
from functools import singledispatchmethod
from typing import Self

from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from ...dispatcher.dispatcher_info import DispatcherType
from ...display.variable.processor.base_process_handler import BaseProcessor
from ...style.palette import RichColors
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


@dataclass(frozen=True, slots=True)
class VariableItemSpec:
    title: str
    key: str
    path_name_only: bool = False


@dataclass(slots=True)
class VariableItemProcessor(BaseProcessor):
    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    items: tuple[VariableItemSpec, ...] = field(default_factory=tuple)
    leading_newline: bool = False
    type: str = field(init=False)

    def __post_init__(self) -> None:
        self.dispatcher_type = DispatcherType[self.type.upper()].value
        super().__post_init__()

    @singledispatchmethod
    def set_items(self, value) -> Self:
        raise TypeError(f"Unsupported item type: {type(value)!r}")

    @set_items.register
    def _(self, value: str) -> Self:
        self.items = (VariableItemSpec(title=value, key=value),)
        return self

    @set_items.register
    def _(self, value: tuple) -> Self:
        self.items = tuple(self._coerce_item(item) for item in value)
        return self

    def set_item(self, title: str, key: str) -> Self:
        self.items = (VariableItemSpec(title=title, key=key),)
        return self

    def with_leading_newline(self) -> Self:
        self.leading_newline = True
        return self

    def _coerce_item(
        self, item: str | tuple[str, str] | VariableItemSpec
    ) -> VariableItemSpec:
        match item:
            case VariableItemSpec():
                return item
            case str():
                return VariableItemSpec(title=item, key=item)
            case (title, key):
                return VariableItemSpec(title=str(title), key=str(key))
            case _:
                raise TypeError(f"Invalid variable item: {item!r}")

    def process_items(self) -> Self:
        builder = VariableTableBuilder(indent=3)

        if self.leading_newline:
            builder.newline()

        for item in self.items:
            value = str(self.get_value_by_key(item.key))
            if item.path_name_only:
                value = Path(value).name

            data = VariableItemContainer(title=item.title, value=value)
            builder.add(data.title, data.value)

        builder.render()
        return self


# Directory names


def set_ota_file_directory(
    processing_function: VariableManager,
) -> None:
    """Sets the OTA file directory in the processing function."""

    from ..variable.processor.file_process_handler import VariableFileProcessor

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

    from ..variable.processor.directory_process_handler import (
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

    from ..variable.processor.directory_process_handler import (
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

    from ..variable.processor.file_process_handler import VariableFileProcessor

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

    from ..variable.processor.file_process_handler import (
        FileIterationProcessor,
    )

    (
        FileIterationProcessor(processing_function)
        .set_file_names(("payload", "stock", "magisk"))
        .process_items()
    )


def set_log_file(processing_function: VariableManager) -> None:
    """Sets the log file in the processing function."""

    from ..variable.processor.file_process_handler import VariableFileProcessor

    (
        VariableFileProcessor(processing_function)
        .set_title("log_file")
        .set_value("log_file")
        .process_items()
    )


# Signed off by Brian Sanford on 20260510
