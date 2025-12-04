# src/variables/variable_manager.py
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Self

import src.components.directory.types.definitions as directory_type_defs
import src.components.directory.types.managers as directory_type_mgrs
import src.dispatchers as dispatchers
import src.structures as structures
import src.types.boot_image as boot_image
import src.validation as validation
from src.logger import logger

magisk_instance = structures.MagiskStruct()

DirectoryTypeDefinition = directory_type_defs.DefaultTypeDefinition
DirectoryTypeManager = directory_type_mgrs.DefaultTypeManager


@dataclass
class VariableManager(object):
    _file_path: Path = field(init=False, repr=False)
    file_stem: Path = field(init=False)
    file_name_parser: structures.FileNameParser = field(init=False)
    log_file: str = field(init=False)
    ota_parent_path: Path = field(init=False)
    boot_image_path: Path = field(init=False, default_factory=Path)
    directory: DirectoryTypeDefinition | None = field(init=False)
    remote_magisk_path: Path = field(
        init=False, default=magisk_instance.remote_path
    )
    path: Path = field(default_factory=Path)
    variables: dict = field(default_factory=dict)
    directories: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.define_variables()
        self.define_directories()
        self.define_files()

    def define_variables(self) -> Self:
        from src.variables.functions import parse_file_name

        self._file_path = validation.file_path_validator(self.path)
        self.patched_image_name = "place_holder"
        self.file_stem = Path(self._file_path.stem)
        self.file_name_parser = parse_file_name(self.file_stem)
        self.variables["patched_image_name"] = "place_holder"
        return self

    def define_files(self) -> Self:
        from src.variables.functions import set_log_file

        self.boot_image_enum = Enum(
            "BootImages", {"MAGISK": Path(self.boot_image_path / "magisk")}
        )
        self.boot_image_struct = boot_image.DefaultImageTypeManager(
            self.file_name_parser,
            str(self.boot_image_path),
        )
        self.boot_image_paths = boot_image.DefaultImageTypeManager(
            self.file_name_parser,
            str(self.boot_image_path),
        )
        self.device_name = self.file_name_parser.device
        self.payload_image_path = self.boot_image_paths.payload.file_path
        self.stock_image_path = self.boot_image_paths.stock.file_path
        self.magisk_image_path = self.boot_image_paths.magisk.file_path
        self.log_file = set_log_file(self.file_name_parser)
        return self

    def define_directories(self) -> Self:
        self.ota_parent_directory = self._file_path.parent
        self.directory = DirectoryTypeManager(
            self._file_path.parent
        ).create_directory()
        return self

    def create_directory(self) -> DirectoryTypeDefinition | None:
        try:
            return DirectoryTypeDefinition(
                self.ota_parent_path,
                str(self.boot_image_path),
                self.remote_magisk_path,
            )
        except Exception as e:
            logger.error(f"[Error] Directory Creation Failed: {e}")
            return None

    def get_dispatcher(
        self, process_type
    ) -> dispatchers.DispatcherInterface | None:
        from src.variables.functions import set_variable_manager

        function_call = set_variable_manager(self.path)
        return (
            DispatcherRetriever(process_type)
            .set_function_call(function_call)
            .get_dispatcher()
        )


class DispatcherTypes(Enum):
    DIRECTORY = "directory"
    FILE = "file"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return self.value


@dataclass
class DispatcherRetriever(object):
    process_type: str

    class DispatcherTypes(Enum):
        DIRECTORY = "directory"
        FILE = "file"
        VARIABLE = "variable"

        def __str__(self) -> str:
            return self.value

    def allowed_dispatchers(self) -> tuple:
        return tuple(enum.value for enum in DispatcherTypes)

    def set_function_call(self, function_call) -> Self:
        self.function_call = function_call
        return self

    def get_dispatcher(self) -> dispatchers.DispatcherInterface | None:
        if self.process_type in self.allowed_dispatchers():
            return (
                dispatchers.DispatcherInterface(
                    self.process_type, self.function_call
                )
                or None
            )


if __name__ == "__main__":
    path = Path("/path/to/your/file")
    from src.variables.functions import set_variable_manager

    variable_manager = set_variable_manager(path)
    print(variable_manager.log_file)
