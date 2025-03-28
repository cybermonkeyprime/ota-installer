from dataclasses import dataclass, field
from pathlib import Path

import build.variables as variables
import build.display.processors as display_processors

VariableManager = variables.VariableManager


@dataclass
class OTAFileNameProcessor(
    display_processors.VariableItemProcessor
):  # takes vars from argparse
    title: str = "ota_file_name"
    value: str = "path.name"


@dataclass
class FileNamesProcessor(display_processors.FileIterationProcessor):
    files: tuple[str, ...] = field(
        default_factory=lambda: ("payload", "stock", "magisk")
    )


@dataclass
class OTADirectoryProcessor(
    display_processors.VariableItemProcessor
):  # takes vars from argparse
    title: str = "ota_file_directory"
    value: str = "path.parent"  # change for debugging


@dataclass
class BootImageDirectoriesProcessor(display_processors.DirectoryIterationProcessor):
    directories: tuple[str, ...] = field(default_factory=lambda: ("stock", "magisk"))
    directory_type: str = "boot_image"


@dataclass
class MagiskImageDirectoriesProcessor(display_processors.DirectoryIterationProcessor):
    directories: tuple[str, ...] = field(default_factory=lambda: ("local", "remote"))
    directory_type: str = "magisk"
    variable_prefix: str = "magisk_"


@dataclass
class LogFileProcessor(display_processors.VariableItemProcessor):
    title: str = "log_file"
    value: str = "log_file"


if __name__ == "__main__":
    variable_manager = VariableManager(Path("some_directory/some_file"))
    display_processor = VariableProcessor(variable_manager)
    display_processor.initiate_processing()
