from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from build.components.file.structures import FileNameParserStructure

from . import BootImageTypeDefinition


@dataclass
class BootImageTypeManager(object):
    filename_parser: type = field(default_factory=lambda: FileNameParserStructure)
    boot_image_directory: Path = field(default_factory=Path)

    def create_image(self) -> Optional[BootImageTypeDefinition]:
        try:
            return BootImageTypeDefinition(
                self.filename_parser, self.boot_image_directory
            )
        except Exception as error:
            raise ValueError(f"Something happened: {error}") from error
