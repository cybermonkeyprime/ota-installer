from dataclasses import dataclass, field

import build.components.directory as directory_component
import build.display.display_data_processors as display_data_processors
import build.variables as variables

VariableManager = variables.VariableManager


@dataclass
class DataProcessor:
    """A class that processes data using provided data processors."""

    process_variable: VariableManager = field(default_factory=VariableManager)
    data_processors: "tuple[type,...]" = field(default_factory=tuple)

    def iterate_data_processors(self) -> "list[type]":
        return [
            item_processor(self.process_variable)
            for item_processor in self.data_processors
        ]


@dataclass
class VariableProcessor(object):
    """A class that handles the processing of variables, files,
    and directories."""

    variable_manager: VariableManager = field(default_factory=VariableManager)

    file_processors: tuple = (
        display_data_processors.OTAFileNameProcessor,
        display_data_processors.FileNamesProcessor,
    )
    directory_processors: tuple = (
        directory_component.OTADirectoryProcessor,
        directory_component.BootImageDirectoriesProcessor,
        directory_component.MagiskImageDirectoriesProcessor,
    )

    def initiate_processing(self) -> None:
        self.process_directories()
        self.process_file_names()
        self.process_log_file()

    def process_file_names(self):
        file_name_processor = DataProcessor(
            process_variable=self.variable_manager,
            data_processors=self.file_processors,
        )
        file_name_processor.iterate_data_processors()
        print()

    def process_directories(self) -> None:
        display_data_processor = DataProcessor(
            process_variable=self.variable_manager,
            data_processors=self.directory_processors,
        )
        display_data_processor.iterate_data_processors()
        print()

    def process_log_file(self) -> None:
        LogFileProcessManager(self.variable_manager)


@dataclass
class DirectoryProccessManager(object):
    variable_manager: VariableManager = field(default_factory=VariableManager)
    directory_processors: tuple = field(default_factory=tuple)

    def __post_init__(self) -> None:
        display_data_processor = DataProcessor(
            self.variable_manager, self.directory_processors
        )
        display_data_processor.iterate_data_processors()
        print()


@dataclass
class LogFileProcessManager(object):
    variable_manager: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        display_data_processors.LogFileProcessor(self.variable_manager)
        print()
