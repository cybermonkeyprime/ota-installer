from dataclasses import dataclass, field

from build.dispatchers import MainDispatcher

import build.display.base_classes as display_base_classes
import build.display.processors as display_processors
import build.variables as variables

VariableManager = variables.VariableManager


@dataclass
class DirectoryError(object):
    """Represents an error that occurred during directory processing."""

    directory_name: str = field(default="")
    error: Exception = field(default_factory=Exception)

    def __str__(self) -> str:
        return f"Error processing directory {self.directory_name}: {self.error}"


@dataclass
class DirectoryHandler:
    """Handles processing of a single directory."""

    dispatch_handler: MainDispatcher = field(default_factory=MainDispatcher)
    process_variable: VariableManager = field(default_factory=VariableManager)
    directory_name: str = field(default="")
    variable_prefix: str = field(default="")

    @property
    def validator(self) -> display_base_classes.ValueValidation:
        return display_base_classes.ValueValidation(self.dispatch_handler)

    def format_directory_title(self, title: str):
        return f"{self.variable_prefix}{title}_directory"

    def validate_directory_value(self, directory_key: str):
        return self.validator.validate_value(key=directory_key)

    def output_formatter(self, directory_name: str = ""):
        return display_base_classes.OutputFormatter(
            title=self.format_directory_title(directory_name),
            value=self.validate_directory_value(directory_name),
        )

    def process_directory(self):
        try:
            formatter = self.output_formatter(self.directory_name)
            formatter.format_and_print()
        except Exception as error:
            print(DirectoryError(self.directory_name, error))


@dataclass
class DirectoryProcessor(object):
    """Processes a group of directories using a dispatch handler and a processing function."""

    directories: tuple[str, ...] = field(default_factory=tuple[str, ...])
    dispatch_handler: MainDispatcher = field(default_factory=MainDispatcher)
    process_variable: VariableManager = field(default_factory=VariableManager)
    variable_prefix: str = field(default="")

    def process_directories(self) -> None:
        [self.process_directory(directory) for directory in self.directories]

    @property
    def validator(self) -> display_base_classes.ValueValidation:
        return display_base_classes.ValueValidation(
            self.dispatch_handler,
        )

    def process_directory(self, directory_name: str):
        directory_handler = DirectoryHandler(
            self.dispatch_handler, self.process_variable, directory_name
        )
        directory_handler.process_directory()


if __name__ == "__main__":
    # Example usage
    variable_manager = VariableManager()
    directories_to_process = ("/path/to/dir1", "/path/to/dir2")
    directory_iteration_processor = display_processors.DirectoryIterationProcessor(
        variable_manager=variable_manager, directories=directories_to_process
    )
