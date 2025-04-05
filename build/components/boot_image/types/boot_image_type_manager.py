from dataclasses import dataclass, field
from typing import Optional

from . import BootImageTypeDefinition
from build.components.file.structures import FileNameParserStructure


@dataclass
class BootImageTypeManager(object):
    filename_parser: type[FileNameParserStructure] = field(
        default_factory=lambda: FileNameParserStructure
    )
    boot_image_directory: str = field(default_factory=str)

    def create_image(self) -> Optional[BootImageTypeDefinition]:
        try:
            return BootImageTypeDefinition(
                self.filename_parser, self.boot_image_directory
            )
        except Exception as error:
            print(f"Something happened: {error}")
            return None
