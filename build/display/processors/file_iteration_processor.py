from dataclasses import dataclass, field

import build.variables as variables


@dataclass
class FileIterationProcessor(object):
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    files: tuple[str, ...] = field(default_factory=lambda: ("", ""))

    def __post_init__(self) -> None:
        self.process_files()

    def process_files(self) -> None:
        for file_name in self.files:
            FileProcessor(self.processing_function, file_name)


@dataclass
class FileProcessor(object):
    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    file_name: str = field(default="")

    @property
    def dispatcher(self) -> type:
        return self.processing_function.get_dispatcher("file")

    @property
    def value(self) -> type:
        return self.dispatcher.get_value(key=self.file_name)

    def __post_init__(self) -> None:
        self.process_file()

    def process_file(self) -> None:
        import build.display.base_classes as dbc

        try:
            processor = dbc.OutputFormatter(
                title=f"{self.file_name}_name", value=self.value.file_name
            )
            processor.format_and_print()
        except Exception as error_msg:
            print(f"?{dbc.ErrorMessage('file', self.file_name, error_msg)}")
