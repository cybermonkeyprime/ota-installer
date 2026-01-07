# src/ota_installer/display/variables/processors/file_iteration_processor.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....variables.variable_manager import VariableManager
from ...variables.processors import BaseProcessor


@dataclass
class FileIterationProcessor(BaseProcessor):
    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    file_names: tuple = field(init=False)

    def set_file_names(self, files: tuple) -> Self:
        self.file_names = tuple(files)
        return self

    def __post_init__(self) -> None:
        self.dispatcher_type = DispatcherConstants.FILE.value
        super().__post_init__()  # initialize dispatcher

    def process_items(self) -> None:
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
