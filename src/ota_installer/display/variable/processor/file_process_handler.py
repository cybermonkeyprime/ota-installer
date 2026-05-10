# src/ota_installer/display/variables/processors/file_processor.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ....dispatcher.dispatcher_type import DispatcherType
from ....variable.variable_manager import VariableManager
from ...variable.processor.base_process_handler import BaseProcessor


@dataclass(slots=True)
class VariableFileProcessor(BaseProcessor):
    """Processes variable files for the dispatcher."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    title: str = field(init=False)
    value: str = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the dispatcher type after the dataclass is created."""
        self.dispatcher_type = DispatcherType.VARIABLE.value
        super().__post_init__()

    def set_title(self, name: str) -> Self:
        """Sets the title of the variable."""
        self.title = name
        return self

    def set_value(self, value: str) -> Self:
        """Sets the value of the variable."""
        self.value = value
        return self

    def process_items(self) -> Self | None:
        """Processes the items and renders the variable table."""
        from ..variable_item_info import VariableItem
        from ..variable_table_builder import VariableTableBuilder

        builder = VariableTableBuilder(indent=3)
        data = VariableItem(
            title=self.title, value=str(self.get_value_by_key(self.value))
        )

        if self.title == "log_file":
            builder.newline()

        builder.add(f"{data.title.upper()}", data.value)
        builder.render()


@dataclass(slots=True)
class FileIterationProcessor(BaseProcessor):
    """Processes a list of file names and builds a variable table."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    file_names: tuple = field(init=False)

    def set_file_names(self, files: tuple) -> Self:
        """Sets the file names to be processed."""
        self.file_names = tuple(files)
        return self

    def __post_init__(self) -> None:
        """Initializes the dispatcher type after the dataclass is created."""
        self.dispatcher_type = DispatcherType.FILE.value
        super().__post_init__()

    def process_items(self) -> None:
        """Processes each file name and builds a variable table."""
        from ..variable_item_info import VariableItem
        from ..variable_table_builder import VariableTableBuilder

        builder = VariableTableBuilder(indent=3)
        for file in self.file_names:
            file_path = str(self.get_value_by_key(key=file))
            data = VariableItem(
                title=f"{file}_name", value=Path(file_path).name
            )
            builder.add(data.title.upper(), str(data.value))
        builder.render()


# Signed off by Brian Sanford on 20260318
