from dataclasses import dataclass, field
from typing import Self

from rich.console import Console
from rich.table import Table

import src.dispatchers.mappings as dispatcher_mappings
import src.display.variables.processors as processors
import src.variables as variables

DispatcherTypeMapping = dispatcher_mappings.DispatcherTypeMapping


@dataclass
class DirectoryIterationProcessor(processors.BaseProcessor):
    processing_function: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )
    directory_names: tuple = field(init=False)
    directory_type: str = field(init=False)
    variable_prefix: str = field(init=False)

    def __post_init__(self):
        self.dispatcher_type = DispatcherTypeMapping.DIRECTORY.value
        super().__post_init__()  # initialize dispatcher

    def set_directory_names(self, directory_names: tuple) -> Self:
        self.directory_names = tuple(directory_names)
        return self

    def set_directory_type(self, directory_type: str) -> Self:
        self.directory_type = str(directory_type)
        return self

    def set_variable_prefix(self, variable_prefix: str) -> Self:
        self.variable_prefix = str(variable_prefix)
        return self

    def process_items(self) -> None:
        for directory in self.directory_names:
            directory_title = (
                f"{self.directory_type}"
                f"{self.variable_prefix}"
                f"{directory}_directory"
            )
            directory_value = f"{self.get_value_by_key(directory)}"
            (
                processors.ItemProcessor()
                .set_item_title("Directory")
                .set_item_name(directory)
                .set_enum_title(directory_title)
                .set_enum_value(directory_value)
                .process_item()
            )
