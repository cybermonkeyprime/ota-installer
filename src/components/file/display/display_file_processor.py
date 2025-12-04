from dataclasses import dataclass, field

import src.dispatchers as dispatchers
from src.dispatchers.dispatcher_mapper import DispatcherType
import src.display.base_classes as display_base_classes
import src.variables as variables


@dataclass
class DisplayFileProcessor(object):
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    data: tuple = field(default_factory=tuple)

    def iterate_files(self):
        for file_processor in self.data:
            return file_processor(self.processing_function)


@dataclass
class DisplayFileIterationProcessor(object):
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    files: tuple[str, ...] = field(default_factory=lambda: ("", ""))

    def __post_init__(self) -> None:
        self.process_files()

    @property
    def dispatch_handler(self) -> dispatchers.DispatcherManager:
        dispatch_handler = display_base_classes.DispatchHandler(
            DispatcherType.FILE, self.processing_function
        )
        return dispatch_handler.create_dispatcher()

    def process_files(self) -> None:
        [self.process_individual_file(file_name=file) for file in self.files]

    def process_individual_file(self, file_name: str) -> None:
        try:
            dispatcher = self.processing_function.get_dispatcher(
                DispatcherType.FILE
            )
            value = dispatcher.get_value(key=file_name)
            processor = display_base_classes.OutputFormatter(
                title=f"{file_name}_name", value=value.file_name
            )
            processor.format_and_print()
        except Exception as error_msg:
            error_message = display_base_classes.ErrorMessage(
                DispatcherType.FILE.name, file_name, error_msg
            )
            print(error_message)
