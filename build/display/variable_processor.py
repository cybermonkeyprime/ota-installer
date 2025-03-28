from dataclasses import dataclass, field

import build.variables as variables
import build.display.data_processors as display_data_processors

VariableManager = variables.VariableManager


@dataclass
class DataProcessor(object):
    """A class that processes data using provided data processors."""

    process_variable: VariableManager = field(default_factory=VariableManager)
    data_processors: tuple = field(default_factory=tuple)

    def iterate_data_processors(self) -> list:
        return [
            item_processor(self.process_variable)
            for item_processor in self.data_processors
        ]


@dataclass
class VariableProcessor(object):
    """A class that handles the processing of variables, files, and directories."""

    variable_manager: VariableManager = field(default_factory=VariableManager)
    file_processors: tuple = (
        display_data_processors.OTAFileNameProcessor,
        display_data_processors.FileNamesProcessor,
    )
    directory_processors: tuple = (
        display_data_processors.OTADirectoryProcessor,
        display_data_processors.BootImageDirectoriesProcessor,
        display_data_processors.MagiskImageDirectoriesProcessor,
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
        display_data_processors.LogFileProcessor(self.variable_manager)
        print()
