from dataclasses import dataclass, field
from typing import Tuple

from build import dispatchers
from dispatchers import DispatcherManager

import build.variables as variables
import build.display.base_classes as display_base_classes


@dataclass
class FileProcesser(object):
    function: type = field(default_factory=lambda: variables.VariableManager)
    data: tuple = field(default_factory=tuple)

    def iterate_files(self) -> list:
        return [file_processor(self.function) for file_processor in self.data]


@dataclass
class FileIterationProcessor(object):
    processing_function: type = field(default_factory=lambda: variables.VariableManager)
    files: Tuple[str, ...] = field(default_factory=lambda: ("", ""))

    def __post_init__(self) -> None:
        self.process_files()

    @property
    def dispatch_handler(self) -> DispatcherManager:
        dispatch_handler = display_base_classes.DispatchHandler(
            "file", self.processing_function
        )
        return dispatch_handler.create_dispatcher()

    def process_files(self) -> None:
        [self.process_individual_file(file_name=file) for file in self.files]

    def process_individual_file(self, file_name: str) -> None:
        try:
            dispatcher = self.processing_function.get_dispatcher("file")
            value = dispatcher.get_value(key=file_name)
            processor = display_base_classes.OutputFormatter(
                title=f"{file_name}_name", value=value.file_name
            )
            processor.format_and_print()
        except Exception as error_msg:
            print(f"?{display_base_classes.ErrorMessage('file', file_name, error_msg)}")
