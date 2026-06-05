from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

from ....variable.variable_manager import VariableManager
from ...variable.variable_functions import (
    set_boot_image_directories,
    set_image_file_names,
    set_log_file,
    set_magisk_image_directories,
    set_ota_file_directory,
    set_ota_file_name,
)


@dataclass(slots=True)
class VariableProcessor:
    """Processes variable file and directory names for OTA installation."""

    variable_manager: VariableManager

    def process_file_names(self) -> Self:
        """Processes OTA and image file names."""
        self._process_items({set_ota_file_name, set_image_file_names})
        return self

    def process_directory_names(self) -> Self:
        """Processes OTA, boot image, and Magisk image directory names."""
        directory_types: set[Callable] = {
            set_ota_file_directory,
            set_boot_image_directories,
            set_magisk_image_directories,
        }
        self._process_items(directory_types)
        print()
        return self

    def _process_items(self, functions: set[Callable]) -> None:
        """Executes a set of processing functions."""
        for function in functions:
            function(self.variable_manager)

    def process_log_file(self) -> Self:
        """Processes the log file."""
        set_log_file(self.variable_manager)
        print()
        return self
