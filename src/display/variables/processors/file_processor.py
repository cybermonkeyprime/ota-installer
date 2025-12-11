# src/display/variables/processors/file_processor.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

import src.dispatchers.mappings as dispatcher_mappings
import src.display.variables.processors as processors
import src.variables as variables

DispatcherTypeMapping = dispatcher_mappings.DispatcherTypeMapping


class VariableFileConstants(Enum):
    TITLE = str
    VALUE = str


@dataclass
class VariableFileProcessor(processors.BaseProcessor):
    processing_function: variables.VariableManager = field(
        default_factory=variables.VariableManager
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
        from ..classes import VariableItemDict, VariableTableBuilder

        builder = VariableTableBuilder(indent=3)
        data = VariableItemDict(
            title=self.title, value=str(self.get_value_by_key(self.value))
        )
        if self.title == "log_file":
            builder.newline()
        builder.add(f"{data.get('title').upper()}", data.get("value"))
        builder.render()
