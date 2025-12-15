# src/ota_installer/display/variables/processors/directory_iteration_processor.py
from dataclasses import dataclass, field
from typing import Self

from ....dispatchers.mappings import DispatcherTypeMapping
from ....variables import VariableManager
from ...variables.processors import BaseProcessor


@dataclass
class DirectoryIterationProcessor(BaseProcessor):
    processing_function: VariableManager = field(
        default_factory=VariableManager
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
        from ..classes import VariableItem, VariableTableBuilder

        builder = VariableTableBuilder(indent=3)
        for directory in self.directory_names:
            data = VariableItem(
                title=f"{self.directory_type}{self.variable_prefix}{directory}_directory",
                value=str(self.get_value_by_key(directory)),
            )
            builder.add(data.title.upper(), data.value)
        builder.render()
