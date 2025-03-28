from dataclasses import dataclass, field

from build.exceptions import error_messages
from dispatchers import MainDispatcher

import build.variables as variables
import build.display.base_classes as display_base_classes

VariableManager = variables.VariableManager


@dataclass
class FileIterationProcessor(object):
    processing_function: VariableManager = field(default_factory=VariableManager)
    files: tuple[str, ...] = field(default_factory=lambda: ("", ""))

    def __post_init__(self) -> None:
        self.process_files()

    @property
    def dispatch_handler(self) -> MainDispatcher:
        dispatch_handler = display_base_classes.DispatchHandler(
            "file", self.processing_function
        )
        return dispatch_handler.create_dispatcher()

    def process_files(self) -> None:
        for file in self.files:
            try:
                dispatcher = self.processing_function.get_dispatcher("file")
                value = dispatcher.get_value(key=file)
                processor = display_base_classes.OutputFormatter(
                    title=f"{file}_name", value=value.file_name
                )
                processor.format_and_print()
            except Exception as error_msg:
                print(display_base_classes.ErrorMessage("file", file, error_msg))


@dataclass
class FileProcesser(object):
    function: VariableManager = field(default_factory=VariableManager)
    data: tuple = field(default_factory=tuple)

    def iterate_files(self) -> list:
        return [file_processor(self.function) for file_processor in self.data]
