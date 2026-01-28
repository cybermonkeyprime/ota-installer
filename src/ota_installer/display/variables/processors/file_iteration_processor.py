# src/ota_installer/display/variables/processors/file_iteration_processor.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....variables.variable_manager import VariableManager
from ...variables.processors.base_processor import BaseProcessor


@dataclass
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
        self.dispatcher_type = DispatcherConstants.FILE.value
        super().__post_init__()

    def process_items(self) -> None:
        """Processes each file name and builds a variable table."""
        from ..classes.variable_table_builder import VariableTableBuilder
        from ..containers.variable_item import VariableItem

        builder = VariableTableBuilder(indent=3)
        for file in self.file_names:
            file_path = str(self.get_value_by_key(key=file))
            data = VariableItem(
                title=f"{file}_name", value=Path(file_path).name
            )
            builder.add(data.title.upper(), data.value)
        builder.render()


