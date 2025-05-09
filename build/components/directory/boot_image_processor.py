from dataclasses import dataclass, field
from typing import Tuple

import build.dispatchers as dispatchers
import build.display.base_classes as display_base_classes
import build.display.processors as display_processors
import build.variables as variables


@dataclass
class OTADirectoryProcessor(
    display_processors.VariableItemProcessor
):  # takes vars from argparse
    title: str = "ota_file_directory"
    value: str = "path.parent"  # change for debugging


@dataclass
class BootImageDirectoriesProcessor(display_processors.DirectoryIterationProcessor):
    directories: Tuple[str, ...] = field(default_factory=lambda: ("stock", "magisk"))
    directory_type: str = "boot_image_path"


@dataclass
class MagiskImageDirectoriesProcessor(display_processors.DirectoryIterationProcessor):
    directories: Tuple[str, ...] = field(default_factory=lambda: ("local", "remote"))
    directory_type: str = "magisk"
    variable_prefix: str = "magisk_"


@dataclass
class DirectoryIterationProcessor(object):
    """Iterates over directories and processes them using a specified dispatch handler."""

    variable_manager: type = field(default_factory=lambda: variables.VariableManager)
    directories: Tuple[str, ...] = field(default_factory=lambda: ("", ""))
    variable_prefix: str = field(default="")
    dispatcher_type: str = field(default="directory")

    def __post_init__(self) -> None:
        self.process_directories()

    @property
    def dispatch_handler(self) -> dispatchers.DispatcherManager:
        dispatch_handler = display_base_classes.DispatchHandler(
            self.dispatcher_type, self.variable_manager
        )
        return dispatch_handler.create_dispatcher()

    def process_directories(self) -> None:
        directory_processor = display_processors.DirectoryProcessor(
            self.directories, self.dispatch_handler, self.variable_manager
        )
        directory_processor.process_directories()
