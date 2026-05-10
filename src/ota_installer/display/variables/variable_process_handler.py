# src/ota_installer/display/display_variable_processor.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Self

from ...dispatchers.dispatcher_type import DispatcherType
from ...types.dispatcher_protocol import DispatcherProtocol
from ...variables.variable_manager import VariableManager
from ..variables.variable_functions import (
    set_boot_image_directories,
    set_image_file_names,
    set_log_file,
    set_magisk_image_directories,
    set_ota_file_directory,
    set_ota_file_name,
)
from .variable_item_info import VariableItem
from .variable_table_builder import VariableTableBuilder


@dataclass
class BaseProcessor(object):
    """Base class for processing with a dispatcher."""

    processing_function: object = field(init=False)
    dispatcher: DispatcherProtocol = field(init=False)
    dispatcher_type: str | None = None  # To be set in subclasses

    def __post_init__(self) -> None:
        """Initializes the dispatcher based on the dispatcher type."""
        if not self.dispatcher_type:
            raise ValueError(
                "dispatcher_type must be set in subclass before __post_init__"
            )

        self.dispatcher = self.processing_function.get_dispatcher(
            self.dispatcher_type
        )

        if not self.dispatcher:
            raise RuntimeError(
                "Dispatcher creation failed for process type: "
                "f{self.dispatcher_type}"
            )

    def get_value_by_key(self, key: str) -> object:
        """Retrieves a value from the dispatcher using the provided key."""
        return self.dispatcher.get_value(key)


@dataclass
class VariableProcessor(object):
    """Processes variable file and directory names for OTA installation."""

    variable_manager: VariableManager

    def process_file_names(self) -> Self:
        """Processes OTA and image file names."""
        file_types = {set_ota_file_name, set_image_file_names}
        self._process_items(file_types)
        return self

    def process_directory_names(self) -> Self:
        """Processes OTA, boot image, and Magisk image directory names."""
        directory_types = {
            set_ota_file_directory,
            set_boot_image_directories,
            set_magisk_image_directories,
        }
        self._process_items(directory_types)
        print()
        return self

    def _process_items(self, functions: set) -> None:
        """Executes a set of processing functions."""
        for function in functions:
            function(self.variable_manager)

    def process_log_file(self) -> Self:
        """Processes the log file."""
        set_log_file(self.variable_manager)
        print()
        return self


#  File
@dataclass(slots=True)
class VariableFileProcessor(BaseProcessor):
    """Processes variable files for the dispatcher."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    title: str = field(init=False)
    value: str = field(init=False)

    def __post_init__(self) -> None:
        """Initializes the dispatcher type after the dataclass is created."""
        self.dispatcher_type = DispatcherType.VARIABLE.value
        super().__post_init__()

    def set_title(self, name: str) -> Self:
        """Sets the title of the variable."""
        self.title = name
        return self

    def set_value(self, value: str) -> Self:
        """Sets the value of the variable."""
        self.value = value
        return self

    def process_items(self) -> Self | None:
        """Processes the items and renders the variable table."""
        from ..variables.variable_item_info import VariableItem
        from ..variables.variable_table_builder import (
            VariableTableBuilder,
        )

        builder = VariableTableBuilder(indent=3)
        data = VariableItem(
            title=self.title, value=str(self.get_value_by_key(self.value))
        )

        if self.title == "log_file":
            builder.newline()

        builder.add(f"{data.title.upper()}", data.value)
        builder.render()


@dataclass(slots=True)
class FileIterationProcessor(BaseProcessor):
    """Processes a list of file names and builds a variable table."""

    processing_function: VariableManager = field(
        default_factory=VariableManager
    )
    file_names: tuple = field(init=False)

    def set_file_names(self, files: tuple) -> Self:
        """Sets the file names to be processed."""
        self.file_names = tuple(files)
        return self

    def __post_init__(self) -> None:
        """Initializes the dispatcher type after the dataclass is created."""
        self.dispatcher_type = DispatcherType.FILE.value
        super().__post_init__()

    def process_items(self) -> None:
        """Processes each file name and builds a variable table."""
        from .variable_item_info import VariableItem
        from .variable_table_builder import VariableTableBuilder

        builder = VariableTableBuilder(indent=3)
        for file in self.file_names:
            file_path = str(self.get_value_by_key(key=file))
            data = VariableItem(
                title=f"{file}_name", value=Path(file_path).name
            )
            builder.add(data.title.upper(), str(data.value))
        builder.render()


# directory
class DirectoryItemType(Enum):
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
        if not key:
            raise AttributeError(
                f"Invalid field: '{field_name}'. "
                f"Allowed fields are: {', '.join(cls._member_names_)}"
            ) from None

        return cls[field_name.upper()].value


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
        self.dispatcher_type = DispatcherType.DIRECTORY.value
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


if __name__ == "__main__":
    pass
