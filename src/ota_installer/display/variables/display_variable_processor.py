# src/ota_installer/display/display_variable_processor.py
from dataclasses import dataclass
from typing import Self

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
    processing_function: VariableManager

    def process_file_names(self) -> Self:
        file_types = {set_ota_file_name, set_image_file_names}
        self.process_items(file_types)
        return self

    def process_directory_names(self) -> Self:
        directory_types = {
            set_ota_file_directory,
            set_boot_image_directories,
            set_magisk_image_directories,
        }
        self.process_items(directory_types)
        print()
        return self

    def process_items(self, iterator: set) -> None:
        function = self.processing_function
        {process_item(function) for process_item in iterator}

    def process_log_file(self) -> Self:
        set_log_file(self.processing_function)
        print()
        return self


if __name__ == "__main__":
    pass
