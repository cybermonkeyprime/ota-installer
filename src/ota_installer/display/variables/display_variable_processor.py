# src/ota_installer/display/display_variable_processor.py
from dataclasses import dataclass, field
from typing import Self

from ...types.dispatcher_protocol import DispatcherProtocol
from ...variables.variable_manager import VariableManager
from ..variables.functions import (
    set_boot_image_directories,
    set_image_file_names,
    set_log_file,
    set_magisk_image_directories,
    set_ota_file_directory,
    set_ota_file_name,
)


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


if __name__ == "__main__":
    pass
