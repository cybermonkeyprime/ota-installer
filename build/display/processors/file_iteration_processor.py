from dataclasses import dataclass, field

import build.variables as variables
from build.dispatchers import DispatcherType


@dataclass
class FileIterationProcessor(object):
    """
    A class responsible for processing multiple files using a given function.

    Attributes:
        process_function: A callable that processes a file.
        files: A tuple of file names to be processed.
    """

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
    """
    A class responsible for processing a single file using a given function.

    Attributes:
        process_function: A callable that processes a file.
        file_name: The name of the file to be processed.
    """

    processing_function: type = field(
        default_factory=lambda: variables.VariableManager
    )
    file_name: str = field(default="")

    @property
    def dispatcher(self) -> type:
        return self.processing_function.get_dispatcher(DispatcherType.FILE)

    @property
    def value(self) -> type:
        return self.dispatcher.get_value(self.file_name)

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
            print(
                f"?{dbc.ErrorMessage(DispatcherType.FILE, self.file_name, error_msg)}"
            )


def main():
    pass


if __name__ == "__main__":
    main()
