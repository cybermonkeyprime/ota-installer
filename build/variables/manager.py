from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as definitions
import build.types.managers as managers

magisk_instance = structures.MagiskStruct()


@dataclass
class VariableManager:
    _file_path: Path = field(init=False, repr=False)
    file_stem: str = field(init=False)
    file_name_parser: structures.FileNameParser = field(init=False)
    boot_image_struct: Optional[definitions.ImageFile] = field(init=False)
    # patched_image_name: str = field(init=False)
    log_file: "LogFile" = field(init=False)
    ota_parent_path: Path = field(init=False)
    boot_image_path: Path = field(
        init=False,
        default_factory=lambda: Path.home() / "Android" / "boot-images",
        # default_factory=lambda: Path(BootImage),
    )
    directory: Optional[definitions.Directory] = field(init=False)
    remote_magisk_path: str = field(
        init=False, default=str(magisk_instance.remote_path)
    )
    path: Path = field(default_factory=Path)
    # user_home_path: Path = field(default_factory=lambda: Path.home())

    def __post_init__(self) -> None:
        self._file_path = FilePathValidator(self.path).validate()
        self.patched_image_name = "place_holder"
        self.initialize_variables()

    def initialize_variables(self) -> None:
        self.file_stem = self._file_path.stem
        self.file_name_parser = structures.FileNameParser(self.file_stem)
        self._define_directories()
        self._define_files()

    def _define_files(self) -> None:
        self.boot_image_struct = managers.ImageFile(
            self.file_name_parser, str(self.boot_image_path)
        ).create_image()
        self.log_file = LogFile(self.file_name_parser)

    def _define_directories(self) -> None:
        self.ota_parent_directory = self._file_path.parent
        self.directory = managers.Directory(self._file_path.parent).create_directory()

    def create_directory(self) -> Optional[definitions.Directory]:
        try:
            return definitions.Directory(
                self.ota_parent_path,
                str(self.boot_image_path),
                self.remote_magisk_path,
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
class FilePathValidator(object):
    file_path: Path

    def validate(self) -> Path:
        posix_file_path = Path(self.file_path)
        if not posix_file_path.exists():
            print(f"Warning, {posix_file_path.stem} does not exist.")
        return posix_file_path


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
