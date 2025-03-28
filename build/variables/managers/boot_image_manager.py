from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as type_managers


@dataclass
class BootImageManager(object):
    """Represents a boot image with its file path and related operations."""

    file_path: Path = field(
        default_factory=lambda: Path.home() / "Android" / "boot-images"
    )

    directory_path: Path = field(default=Path.home() / "Android" / "boot-images")

    @property
    def file_name_parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.file_path.stem)

    def image_file_manager(self) -> Optional[definitions.ImageFile]:
        manager = type_managers.ImageFile(
            self.file_name_parser, f"{self.directory_path}"
        )
        return manager.create_image()

    @property
    def struct(self) -> Optional[definitions.ImageFile]:
        return self.image_file_manager()
