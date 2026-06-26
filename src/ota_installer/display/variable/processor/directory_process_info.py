# src/ota_installer/display/variable/processor/directory_process_info.py
from dataclasses import dataclass, field
from enum import Enum

from ....variable.variable_manager import VariableManager
from ...variable.processor.base_process_info import BaseProcessor


class DirectoryItemInfo(Enum):
    """Constants for task item types."""

    INDEX = int
    TITLE = str
    DESCRIPTION = str
    COMMENT = str
    REMINDER = str
    COMMAND_STRING = str

    @classmethod
    def get_validated_type(cls, field_name: str) -> type:
        """Validates field existence using a whitelist check."""
        if (key := field_name.upper()) not in cls._member_names_:
            raise AttributeError(
                f"Invalid field: '{field_name}'. "
                f"Allowed fields are: {', '.join(cls._member_names_)}"
            ) from None

        return cls[key].value


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
        from ....dispatcher.dispatcher_info import DispatcherType

        self.dispatcher_type = DispatcherType.DIRECTORY.value
        super().__post_init__()

    def process_items(self) -> None:
        """Processes each directory and builds a variable table."""
        from ..variable_item_info import (
            VariableItemContainer,
            VariableTableBuilder,
        )

        builder = VariableTableBuilder(indent=3)
        for directory in self.directory_names:
            title_string = (
                f"{self.directory_type}"
                f"{self.variable_prefix}"
                f"{directory}_directory"
            )
            value_string = str(self.get_value_by_key(directory))
            data = VariableItemContainer(
                title=title_string, value=value_string
            )
            builder.add(data.title.upper(), data.value)
        builder.render()


# Signed off by Brian Sanford on 20260625
