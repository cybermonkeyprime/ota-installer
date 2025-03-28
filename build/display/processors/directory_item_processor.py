from dataclasses import dataclass, field

from build.dispatchers import MainDispatcher

import build.display.base_classes as display_base_classes
import build.display.processors as display_processors
import build.variables as variables

VariableManager = variables.VariableManager


@dataclass
class DirectoryIterationProcessor(object):
    """Iterates over directories and processes them using a specified dispatch handler."""

    variable_manager: variables.VariableManager = field(
        default_factory=lambda: variables.VariableManager()
    )
    directories: tuple[str, ...] = field(default_factory=lambda: ("", ""))
    variable_prefix: str = field(default="")
    dispatcher_type: str = field(default="directory")

    def __post_init__(self) -> None:
        self.process_directories()

    @property
    def dispatch_handler(self) -> MainDispatcher:
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
    variable_manager = variables.VariableManager()
    directory_processor = DirectoryIterationProcessor(
        variable_manager=variable_manager,
        directories=("/path/to/dir1", "/path/to/dir2"),
        variable_prefix="PREFIX_",
        dispatcher_type="custom_directory",
    )
    directory_processor.process_directories()


if __name__ == "__main__":
    main()
