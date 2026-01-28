# src/ota_installer/display/variables/processors/directory_iteration_processor.py
from dataclasses import dataclass, field
from typing import Self

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....variables.variable_manager import VariableManager
from ...variables.processors.base_processor import BaseProcessor


@dataclass
class DirectoryIterationProcessor(BaseProcessor):
    """Processes directory iterations for variable management."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    directory_names: tuple = field(init=False)
    directory_type: str = field(init=False)
    variable_prefix: str = field(init=False)

    def __post_init__(self):
        """Initializes the dispatcher type."""
        self.dispatcher_type = DispatcherConstants.DIRECTORY.value
        super().__post_init__()

    def set_directory_names(self, directory_names: tuple[str, ...]) -> Self:
        """Sets the directory names for processing."""
        self.directory_names = tuple(directory_names)
        return self

    def set_directory_type(self, directory_type: str) -> Self:
        """Sets the type of directories being processed."""
        self.directory_type = str(directory_type)
        return self

    def set_variable_prefix(self, variable_prefix: str) -> Self:
        """Sets the prefix for variable names."""
        self.variable_prefix = str(variable_prefix)
        return self

    def process_items(self) -> None:
        from ..classes.variable_table_builder import VariableTableBuilder
        from ..containers.variable_item import VariableItem

        """Processes each directory and builds a variable table."""
        builder = VariableTableBuilder(indent=3)
        for directory in self.directory_names:
            title_string = (
                f"{self.directory_type}"
                f"{self.variable_prefix}"
                f"{directory}_directory"
            )
            value_string = str(self.get_value_by_key(directory))
            data = VariableItem(title=title_string, value=value_string)
            builder.add(data.title.upper(), data.value)
        builder.render()


