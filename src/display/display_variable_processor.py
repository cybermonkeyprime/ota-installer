from dataclasses import dataclass
from typing import Self

import src.variables as variables
from src.display.variables import (
    set_boot_image_directories,
    set_image_file_names,
    set_log_file,
    set_magisk_image_directories,
    set_ota_file_directory,
    set_ota_file_name,
)


@dataclass
class VariableProcessor(object):
    processing_function: variables.VariableManager

    def process_file_names(self) -> Self:
        for process_item in {set_ota_file_name, set_image_file_names}:
            process_item(self.processing_function)
        return self

    def process_directory_names(self) -> Self:
        for process_item in {
            set_ota_file_directory,
            set_boot_image_directories,
            set_magisk_image_directories,
        }:
            process_item(self.processing_function)
        print()
        return self

    def process_log_file(self) -> Self:
        set_log_file(self.processing_function)
        print()
        return self


if __name__ == "__main__":
    pass
