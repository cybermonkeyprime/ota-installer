from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from decorators import ColorizedIndentPrinter
from dispatchers import MainDispatcher

import build.variables as variables


@dataclass
class VariableProcessor(object):
    processing_function: variables.Manager

    def initiate_processing(self) -> None:
        self.process_directories()
        self.process_file_names()
        self.process_log_file()

    def process_file_names(self) -> None:
        files = {OTAFileNameProcessor, FileNamesProcessor}
        for file_processor in files:
            file_processor(self.processing_function)
        print()

    def process_directories(self) -> None:
        directories = {
            OTADirectoryProcessor,
            BootImageDirectoriesProcessor,
            MagiskImageDirectoriesProcessor,
        }
        for directory_processor in directories:
            directory_processor(self.processing_function)
        print()

    def process_log_file(self) -> None:
        LogFileProcessor(self.processing_function)
        print()


@dataclass
class VariableOutputProcessor(object):
    title: str = field(default="")
    value: str = field(default="")

    @ColorizedIndentPrinter(indent=1)
    def parser(self) -> str:
        return f"{self.title.upper()}: {self.value}"


@dataclass
class FileIterationProcessor(object):
    processing_function: variables.Manager = field(default_factory=variables.Manager)
    files: tuple[str, ...] = field(default_factory=lambda: ("", ""))

    def __post_init__(self) -> None:
        self.process_files()

    def process_files(self) -> None:
        for file in self.files:
            try:
                dispatcher = self.processing_function.get_dispatcher("file")
                value = dispatcher.get_value(key=file)

                processor = VariableOutputProcessor(
                    title=f"{file}_name", value=value.file_name
                )
                processor.parser()
            except Exception as e:
                print(f"Error processing file {file}: {e}")


@dataclass
class VariableItemProcessor(object):
    processing_function: Optional[variables.Manager] = field(default=None)
    title: str = field(default="")
    value: str = field(default="")

    def __post_init__(self) -> None:
        self.process_item()

    def process_item(self) -> None:
        try:
            dispatcher = MainDispatcher("variable", self.processing_function)
            value = dispatcher.get_dispatcher().get_value(key=self.value)
            variable_output = VariableOutputProcessor(title=self.title, value=value)
            variable_output.parser()
        except Exception as e:
            print(f"Error processing variable item {self.title}: {e}")


@dataclass
class DirectoryIterationProcessor(object):
    processing_function: Optional[variables.Manager] = field(default=None)
    directories: tuple[str, ...] = field(default_factory=lambda: ("", ""))
    directory_type: str = field(default="")
    variable_prefix: str = field(default="")

    def __post_init__(self) -> None:
        self.process_directories()

    def process_directories(self) -> None:
        for directory in self.directories:
            try:
                dispatcher = MainDispatcher("directory", self.processing_function)
                value = dispatcher.get_dispatcher().get_value(key=directory)
                title = f"{self.variable_prefix}{directory}_directory"
                formatter = VariableOutputProcessor(title=title, value=value)
                formatter.parser()
            except Exception as e:
                print(f"Error processing directory {directory}: {e}")


@dataclass
class OTAFileNameProcessor(VariableItemProcessor):
    title: str = "ota_file_name"
    value: str = "path.name"


@dataclass
class FileNamesProcessor(FileIterationProcessor):
    files: tuple[str, ...] = field(
        default_factory=lambda: ("payload", "stock", "magisk")
    )


@dataclass
class OTADirectoryProcessor(VariableItemProcessor):
    title: str = "ota_file_directory"
    value: str = "path.parent"


@dataclass
class BootImageDirectoriesProcessor(DirectoryIterationProcessor):
    directories: tuple[str, ...] = field(default_factory=lambda: ("stock", "magisk"))
    directory_type: str = "boot_image"


@dataclass
class MagiskImageDirectoriesProcessor(DirectoryIterationProcessor):
    directories: tuple[str, ...] = field(default_factory=lambda: ("local", "remote"))
    directory_type: str = "magisk"
    variable_prefix: str = "magisk_"


@dataclass
class LogFileProcessor(VariableItemProcessor):
    title: str = "log_file"
    value: str = "log_file"


if __name__ == "__main__":
    variable_manager = variables.Manager(Path("some_directory/some_file"))
    display_processor = DisplayVariableProcessor(variable_manager)
    display_processor.initiate_processing()
