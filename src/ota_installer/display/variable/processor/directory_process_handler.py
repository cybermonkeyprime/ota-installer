# display/variable/processor/directory_process_handler.py
from dataclasses import dataclass, field
from enum import Enum
from typing import Self

from ....variable.variable_manager import VariableManager
from ...variable.processor.base_process_handler import BaseProcessor


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
        """
        Validates field existence using a whitelist check.
        Raises AttributeError immediately on failure (Fail-Fast).
        """
        key = field_name.upper()

        # Explicit membership check: 'Look Before You Leap'
        if key not in cls._member_names_:
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

    def set_directory_names(self, directory_names: tuple[str, ...]) -> Self:
        """Sets the directory names for processing."""
        self.directory_names = directory_names
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
        """Processes each directory and builds a variable table."""
        from ..variable_item_handler import (
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
