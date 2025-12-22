# src/ota_installer/display/variables/processors/file_processor.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from ....dispatchers.mappings import DispatcherTypeMapping
from ....variables import VariableManager
from ...variables.processors import BaseProcessor


class VariableFileConstants(Enum):
    TITLE = str
    VALUE = str


@dataclass
class VariableFileProcessor(BaseProcessor):
    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    title: str = field(init=False)
    value: str = field(init=False)

    def __post_init__(self) -> object | None:
        self.dispatcher_type = DispatcherTypeMapping.VARIABLE.value
        super().__post_init__()  # initialize dispatcher

    def set_title(self, name: str) -> Self:
        self.title = str(name)
        return self

    def set_value(self, value: str) -> Self:
        self.value = str(value)
        return self

    def process_items(self) -> Self | None:
        from ..classes.variable_table_builder import VariableTableBuilder
        from ..containers.variable_item import VariableItem

        builder = VariableTableBuilder(indent=3)
        data = VariableItem(
            title=self.title, value=str(self.get_value_by_key(self.value))
        )
        if self.title == "log_file":
            builder.newline()
        builder.add(f"{data.title.upper()}", data.value)
        builder.render()
