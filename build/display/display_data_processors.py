from dataclasses import dataclass, field

import build.display.processors as display_processors


@dataclass
class OTAFileNameProcessor(
    display_processors.VariableItemProcessor
):  # takes vars from argparse
    title: str = "ota_file_name"
    value: str = "path.name"


@dataclass
class FileNamesProcessor(display_processors.FileIterationProcessor):
    files: "tuple" = field(
        default_factory=lambda: ("payload", "stock", "magisk")
    )


@dataclass
class LogFileProcessor(display_processors.VariableItemProcessor):
    title: str = "log_file"
    value: str = "log_file"


if __name__ == "__main__":
    pass
#    variable_manager = VariableManager(Path("some_directory/some_file"))
#    display_processor = VariableProcessor(variable_manager)
#    display_processor.initiate_processing()
