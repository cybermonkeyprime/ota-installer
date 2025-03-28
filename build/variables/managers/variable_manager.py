from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as type_managers
import build.validation as validation
import build.managers as managers

magisk = structures.MagiskStruct()


@dataclass
class VariableManager(object):
    """Manages variables related to boot images and file operations."""

    path: Path = field(default_factory=Path)

    @property
    def file_name(self) -> "FileNameManager":
        return FileNameManager(path=self.path)

    @property
    def boot_image(self) -> "BootImageManager":
        return BootImageManager(file_path=self.file_name.validator())

    @property
    def patched_image_name(self) -> str:
        return "place_holder"

    @patched_image_name.setter
    def patched_image_name(self, image_name: str) -> bool:
        patched_image_creator = PatchedImageManager(image_name=image_name)
        self.patched_image_name = patched_image_creator.image_name
        return True

    @property
    def log_file(self) -> "LogFileManager":
        return LogFileManager(parser=self.file_name.parser())

    @property
    def directory(self) -> Optional[definitions.Directory]:
        directory_manager = type_managers.Directory(self.file_name.path.parent)
        return directory_manager.create_directory()

    def get_dispatcher(self, object_type: type) -> Optional[dispatchers.MainDispatcher]:
        dispatcher_creation = DispatcherManager(self.path)
        return dispatcher_creation.creator(object_type)


@dataclass
class PatchedImageManager:
    image_name: str = field(default="place_holder")


@dataclass
class DispatcherManager(VariableManager):
    path: Path = field(default_factory=Path)
    allowed_objects: set = field(
        default_factory=lambda: {"directory", "file", "variable"}
    )

    @property
    def variable_manager_instance(self) -> VariableManager:
        return VariableManager(path=self.path)

    def creator(self, object_type) -> Optional[dispatchers.MainDispatcher]:
        try:
            if object_type in self.allowed_objects:
                return dispatchers.MainDispatcher(
                    object_type, self.variable_manager_instance
                )
        except Exception as err:
            print(err)


@dataclass
class FileNameManager(VariableManager):
    @property
    def parts(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)

    def validator(self) -> Path:
        file_path_validation = validation.FilePathValidation(file_path=self.path)
        return file_path_validation.validator()

    def parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)


@dataclass
class BootImageManager(object):
    """Represents a boot image with its file path and related operations."""

    file_path: Path = field(
        default_factory=lambda: Path.home() / "Android" / "boot-images"
    )

    @property
    def file_name_parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.file_path.stem)

    @property
    def image_file_manager(self) -> Optional[definitions.ImageFile]:
        manager = managers.ImageFile(self.file_name_parser, f"{self.file_path}")
        return manager.create_image()

    @property
    def struct(self) -> Optional[definitions.ImageFile]:
        return self.image_file_manager


@dataclass
class LogFileManager(object):
    """Generates a log file name based on the file name parser."""

    parser: Any = field(default_factory=lambda: structures.FileNameParser)

    def __str__(self) -> str:
        return f"/tmp/ota_variables_{self.parser.device}_{self.parser.version}.txt"


if __name__ == "__main__":
    path = "/path/to/your/file"
    variable_manager = VariableManager(path=Path(path))
    print(variable_manager.log_file)
