from dataclasses import dataclass, field

from src.components.file.display import DisplayFileIterationProcessor
from src.display.processors.variable_processors import VariableItemProcessor


@dataclass
class FileNamesProcessor(DisplayFileIterationProcessor):
    files: tuple[str, ...] = field(
        default_factory=lambda: (
            "payload",
            "stock",
            "magisk",
        )
    )

    # @dataclass
    # class OTADirectoryProcessor(
    VariableItemProcessor
    # takes vars from argparse
    title: str = "ota_file_directory"
    value: str = "path.parent"  # change for debugging
