from dataclasses import dataclass, field
from typing import Tuple

import build.display.base_classes as display_base_classes
import build.display.processors as display_processors
from build.dispatchers import DispatcherManager
from build.dispatchers.dispatcher_mapper import DispatcherType


@dataclass
class DirectoryIterationProcessor(object):
    """Iterates over directories and processes them using a specified dispatch
    handler.
    """

    variable_manager: type = field(default_factory=lambda: type)
    directories: Tuple[str, ...] = field(default_factory=lambda: ("", ""))
    variable_prefix: str = field(default="")
    dispatcher_type: DispatcherType = field(default=DispatcherType.DIRECTORY)

    def __post_init__(self) -> None:
        self.process_directories()

    @property
    def dispatch_handler(self) -> DispatcherManager:
        dispatch_handler = display_base_classes.DispatchHandler(
            self.dispatcher_type, self.variable_manager
        )
        return dispatch_handler.create_dispatcher()

    def process_directories(self) -> None:
        directory_processor = display_processors.DirectoryProcessor(
            self.directories, self.dispatch_handler, self.variable_manager
        )
        directory_processor.process_directories()


def main():
    # Example usage
    variable_manager = "variables.VariableManager()"
    directory_processor = DirectoryIterationProcessor(
        variable_manager=variable_manager,
        directories=("/path/to/dir1", "/path/to/dir2"),
        variable_prefix="PREFIX_",
        dispatcher_type="custom_directory",
    )
    directory_processor.process_directories()


if __name__ == "__main__":
    main()
