import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, FilePath, ValidationError

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as managers

magisk = structures.MagiskStruct()


@dataclass
class VariableManager:
    path: Path = field(default_factory=Path)

    @property
    def file_name(self) -> "FileName":
        return FileName(path=self.path)

    @property
    def boot_image(self) -> "BootImage":
        return BootImage(self.file_name.validator)

    @property
    def patched_image_name(self) -> str:
        return "place_holder"

    @property
    def log_file(self) -> "LogFile":
        return LogFile(self.file_name.parser)

    @property
    def directory(self) -> Optional[definitions.Directory]:
        manager = managers.Directory(self.file_name.path.parent)
        return manager.create_directory()

    def create_directory(self) -> Optional[definitions.Directory]:
        try:
            return definitions.Directory(
                self.file_name.path.parent,
                str(self.boot_image.path),
                magisk.remote_path,
            )
        except Exception as e:
            print(f"Error creating directory: {e}")
            return None

    def get_dispatcher(self, object_type) -> Optional[dispatchers.MainDispatcher]:
        variable_manager = VariableManager
        allowed_objects = {"directory", "file", "variable"}  # type list
        if object_type in allowed_objects:
            return dispatchers.MainDispatcher(object_type, variable_manager(self.path))
        else:
            return None


@dataclass
class FileName(object):
    path: Path = field(default=Path(""))

    @property
    def validator(self) -> Path:
        file_path_validator = FilePathValidator(file_path=self.path)
        return file_path_validator.validator()

    @property
    def parser(self) -> structures.FileNameParser:
        return structures.FileNameParser(self.path.stem)


@dataclass
class BootImage(object):
    file_path: Path = field(default=Path(""))

    @property
    def file_name_parser(self):
        return structures.FileNameParser(self.file_path.stem)

    @property
    def path(self) -> Path:
        return Path.home() / "Android" / "boot-images"

    @property
    def struct(self) -> Optional[definitions.ImageFile]:
        manager = managers.ImageFile(self.file_name_parser, str(self.path))
        return manager.create_image()


class FileExistenceModel(BaseModel):
    file_path: FilePath

    def checker(self):
        file_path = Path(self.file_path)
        try:
            file_path.exists()
        except FileNotFoundError:
            print(f"Warning, {file_path.stem} doesn't exist.")
        finally:
            return file_path


@dataclass
class FilePathValidator(object):
    file_path: Path

    def validator(self) -> Path:
        try:
            FileExistenceModel(file_path=self.file_path).checker()
        except ValidationError:
            print(f"Warning, {Path(self.file_path).stem} does not exist.")
            sys.exit()
        else:
            return Path(self.file_path)


@dataclass
class LogFile(object):
    file_name_parser: structures.FileNameParser

    def __str__(self) -> str:
        device = self.file_name_parser.device
        version = self.file_name_parser.version
        return f"/tmp/ota_variables_{device}_{version}.txt"


if __name__ == "__main__":
    path = "/path/to/your/file"
    variable_manager = VariableManager(path=Path(path))
    print(variable_manager.log_file)
