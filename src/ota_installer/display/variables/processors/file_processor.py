# src/ota_installer/display/variables/processors/file_processor.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from ....dispatchers.constants.dispatcher_constants import DispatcherConstants
from ....variables.variable_manager import VariableManager
from ...variables.processors.base_processor import BaseProcessor


class VariableFileConstants(Enum):
    TITLE = str
    VALUE = str


@dataclass
class VariableFileProcessor(BaseProcessor):
    """Processes variable files for the dispatcher."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    title: str = field(init=False)
    value: str = field(init=False)

    def __post_init__(self) -> object | None:
        """Initializes the dispatcher type after the dataclass is created."""
        self.dispatcher_type = DispatcherConstants.VARIABLE.value
        super().__post_init__()

    def set_title(self, name: str) -> Self:
        """Sets the title of the variable."""
        self.title = str(name)
        return self

    def set_value(self, value: str) -> Self:
        """Sets the value of the variable."""
        self.value = str(value)
        return self

    def process_items(self) -> Self | None:
        """Processes the items and renders the variable table."""
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


# Signed off by Brian Sanford on 20260119
