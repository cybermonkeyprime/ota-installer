from dataclasses import dataclass, field

import build.display.processors as display_processors
import build.components.file as file_component


@dataclass
class FileNamesProcessor(file_component.DisplayFileIterationProcessor):
    files: tuple[str, ...] = field(
        default_factory=lambda: ("payload", "stock", "magisk")
    )

    # @dataclass
    # class OTADirectoryProcessor(
    display_processors.VariableItemProcessor
    # takes vars from argparse
    title: str = "ota_file_directory"
    value: str = "path.parent"  # change for debugging
