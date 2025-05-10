from dataclasses import dataclass, field
from pathlib import Path
from typing import Tuple

import build.variables as variables
import build.display.processors as display_processors
# import build.components.directory as directory_component

VariableManager = variables.VariableManager


@dataclass
class OTAFileNameProcessor(
    display_processors.VariableItemProcessor
):  # takes vars from argparse
    title: str = "ota_file_name"
    value: str = "path.name"


@dataclass
class FileNamesProcessor(display_processors.FileIterationProcessor):
    files: Tuple[str, ...] = field(
        default_factory=lambda: ("payload", "stock", "magisk")
    )

    # @dataclass
    # class OTADirectoryProcessor(
    display_processors.VariableItemProcessor
    # takes vars from argparse
    title: str = "ota_file_directory"
    value: str = "path.parent"  # change for debugging


@dataclass
class LogFileProcessor(display_processors.VariableItemProcessor):
    title: str = "log_file"
    value: str = "log_file"


if __name__ == "__main__":
    variable_manager = VariableManager(Path("some_directory/some_file"))
#    display_processor = VariableProcessor(variable_manager)
#    display_processor.initiate_processing()
