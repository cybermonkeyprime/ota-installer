# src/variables/variable_manager.py
from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

import src.dispatchers as dispatchers
import src.structures as structures
import src.types.boot_image as boot_image
import src.types.directory as directory_types
import src.validation as validation
from src.logger import logger
from src.paths.constants import (
    BootImagePaths,
    MagiskImagePaths,
)

DirectoryTypeDefinition = directory_types.DefaultTypeDefinition
DirectoryTypeManager = directory_types.DefaultTypeManager


@dataclass
class VariableManager(object):
    _file_path: Path = field(init=False, repr=False)
    file_stem: Path = field(init=False)
    file_name_bits: structures.FileNameParser = field(init=False)
    log_file: str = field(init=False)
    ota_parent_path: Path = field(init=False)
    boot_image_path: Path = field(init=False, default_factory=Path)
    directory: DirectoryTypeDefinition | None = field(init=False)
    remote_magisk_path: Path = field(
        init=False, default=MagiskImagePaths.REMOTE_PATH.value
    )
    path: Path = field(default_factory=Path)
    files: dict = field(init=False)
    variables: dict = field(default_factory=dict)
    directories: dict = field(default_factory=dict)
    paths: dict = field(default_factory=dict)
    file_name: dict = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.define_variables()
        self.define_directories()
        self.define_files()

    def define_variables(self) -> Self:
        variables = VariableDefiner(self.path).data_tuple

        self._file_path = variables.file_path
        self.patched_image_name = variables.magisk_image_name
        self.file_stem = variables.file_path_stem
        self.file_name_bits = variables.file_parts
        self.file_name_parts = variables.file_parts
        self.file_name["parts"] = variables.file_parts
        self.file_name["device"] = self.file_name["parts"].device
        self.file_name["version"] = self.file_name["parts"].version
        return self

    def define_files(self) -> Self:
        from src.structures import ImageFileData
        from src.variables.functions import get_file_image_path, set_log_file

        image_data = ImageFileData(
            self.file_name["device"], self.file_name["version"]
        )
        self.paths["payload"] = get_file_image_path("payload", *image_data)
        self.paths["stock"] = get_file_image_path("stock", *image_data)
        self.paths["magisk"] = get_file_image_path("magisk", *image_data)
        self.paths["log_file"] = set_log_file(self.file_name_parts)

        return self

    def define_directories(self) -> Self:
        self.ota_parent_directory = self._file_path.parent
        self.directory = DirectoryTypeManager(
            self._file_path.parent
        ).create_directory()
        self.magisk_image_local_path = MagiskImagePaths.REMOTE_PATH.value
        self.magisk_image_remote_path = MagiskImagePaths.REMOTE_PATH.value

        self.directories = defaultdict(dict)
        self.directories["magisk"]["local_path"] = (
            MagiskImagePaths.LOCAL_PATH.value
        )
        self.directories["magisk"]["remote_path"] = (
            MagiskImagePaths.REMOTE_PATH.value
        )
        return self

    def create_directory(self) -> DirectoryTypeDefinition | None:
        try:
            return DirectoryTypeDefinition(
                self.ota_parent_path,
                str(self.boot_image_path),
                self.remote_magisk_path,
            )
        except Exception as err:
            logger.error(
                f"[{type(err).__name__}] Directory Creation Failed: {err}"
            )
            return None

    def get_dispatcher(
        self, process_type
    ) -> dispatchers.DispatcherInterface | None:
        from src.variables.functions import set_variable_manager

        from .classes.dispatch_retriever import DispatchRetriever

        function_call = set_variable_manager(self.path)
        return (
            DispatchRetriever(process_type)
            .set_function_call(function_call)
            .get_dispatcher()
        )


VariableTypeTuple = namedtuple(
    "VariableTypeTuple",
    ["file_path", "magisk_image_name", "file_path_stem", "file_parts"],
)


@dataclass
class VariableDefiner(object):
    file_path: Path

    def __post_init__(self) -> Self:
        from src.variables.functions import parse_file_name

        valid_path = validation.file_path_validator(self.file_path)
        self.data_tuple = VariableTypeTuple(
            file_path=valid_path,
            magisk_image_name="place_holder",
            file_path_stem=Path(valid_path.stem),
            file_parts=parse_file_name(valid_path.stem),
        )
        return self


if __name__ == "__main__":
    path = Path("/path/to/your/file")
    from src.variables.functions import set_variable_manager

    variable_manager = set_variable_manager(path)
    print(variable_manager.log_file)
