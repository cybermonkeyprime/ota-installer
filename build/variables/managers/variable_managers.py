from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as type_managers
import build.validation as validation


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

    @property
    def struct(self) -> Optional[definitions.ImageFile]:
        file_manager = type_managers.ImageFile(
            self.file_name_parser, str(self.directory_path)
        )
        try:
            return file_manager.create_image()
        except Exception as e:
            print(f"Error creating image file: {e}")
            return None


@dataclass
class DispatcherManager(object):
    Class: Callable = field(default_factory=lambda: type)
    path: Path = field(default_factory=Path)
    allowed_objects: set = field(
        default_factory=lambda: {"directory", "file", "variable"}
    )

    def creator(self, object_type) -> Optional[dispatchers.MainDispatcher]:
        try:
            if object_type in self.allowed_objects:
                return dispatchers.MainDispatcher(object_type, self.Class(self.path))
        except Exception as err:
            print(err)


@dataclass
class FileNameManager(object):
    path: Path = field(default_factory=Path)

    @property
    def parts(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)

    def validator(self) -> Path:
        file_path_validation = validation.FilePathValidation(file_path=self.path)
        return file_path_validation.validator()

    def parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)


@dataclass
class LogFileManager(object):
    """Generates a log file name based on the file name parser."""

    parser: Any = field(default_factory=lambda: structures.FileNameParser)

    def __str__(self) -> str:
        return f"/tmp/ota_variables_{self.parser.device}_{self.parser.version}.txt"


@dataclass
class PatchedImageManager:
    image_name: str = field(default="place_holder")
