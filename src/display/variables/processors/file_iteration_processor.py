# src/display/variables/processors/file_iteration_processor.py
from dataclasses import dataclass, field
from typing import Self

import src.dispatchers.mappings as dispatcher_mappings
import src.display.variables.processors as processors
import src.variables as variables

DispatcherTypeMapping = dispatcher_mappings.DispatcherTypeMapping


@dataclass
class FileIterationProcessor(processors.BaseProcessor):
    processing_function: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )
    file_names: tuple = field(init=False)

    def set_file_names(self, files: tuple) -> Self:
        self.file_names = tuple(files)
        return self

    def __post_init__(self) -> None:
        self.dispatcher_type = DispatcherTypeMapping.FILE.value
        super().__post_init__()  # initialize dispatcher

    def process_items(self) -> None:
        for file in self.file_names:
            file_path = self.get_value_by_key(key=file).file_path
            (
                processors.ItemProcessor()
                .set_item_title("File Iteration")
                .set_item_name(file)
                .set_enum_title(f"{file}_name")
                .set_enum_value(file_path.name)
                .process_item()
            )
