# src/ota_installer/variables/variable_manager.py
from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..dispatchers import DispatcherInterface
from ..log_setup import logger
from ..paths.constants import (
    MagiskImagePaths,
)
from ..types.directory import DefaultTypeDefinition, DefaultTypeManager

DirectoryTypeDefinition = DefaultTypeDefinition
DirectoryTypeManager = DefaultTypeManager


@dataclass
class VariableManager(object):
    """Defines all variables"""

    """main entry point"""
    path: Path = field(default_factory=Path)

    """ directory type validation"""
    directory: DirectoryTypeDefinition | None = field(init=False)

    """dicts"""
    file_paths: dict = field(default_factory=dict[str, str], init=False)
    file_name: dict = field(default_factory=dict[str, str], init=False)
    image_name: dict = field(default_factory=dict[str, str], init=False)
    directories: dict = field(
        default_factory=lambda: defaultdict(dict[str, str]), init=False
    )

    def __post_init__(self) -> None:
        self.variables = VariableDefiner(self.path).data_tuple
        self.define_file_name_attributes()
        self.define_file_paths()
        self.define_directory_paths()
        self.define_image_names()

    def define_file_name_attributes(self) -> Self:
        self.file_name = {
            "path": self.variables.file_path,
            "stem": self.variables.file_path_stem,
            "parts": self.variables.file_parts,
            "device": self.variables.file_parts.device,
            "version": self.variables.file_parts.version,
        }
        return self

    def define_file_paths(self) -> Self:
        from ..structures import ImageFileData
        from ..variables.functions import (
            get_file_image_path,
            set_log_file,
        )

        image_data = ImageFileData(
            self.file_name["device"], self.file_name["version"]
        )
        self.file_paths = {
            "stock": get_file_image_path("stock", *image_data),
            "magisk": get_file_image_path("magisk", *image_data),
            "payload": get_file_image_path("payload", *image_data),
            "log_file": set_log_file(self.file_name["parts"]),
        }
        return self

    def define_directory_paths(self) -> Self:
        self.ota_parent_directory = self.path.parent
        self.directory = DirectoryTypeManager(
            self.file_name["path"].parent
        ).create_directory()

        self.directories = {
            "magisk": {
                "local_path": MagiskImagePaths.LOCAL_PATH.value,
                "remote_path": MagiskImagePaths.REMOTE_PATH.value,
            }
        }
        return self

    def define_image_names(self) -> Self:
        self.image_name = {
            "patched": self.variables.magisk_image_name,
        }

        return self

    def create_directory(self) -> DirectoryTypeDefinition | None:
        try:
            return DirectoryTypeDefinition(
                self.path.parent,
                str(self.file_paths["stock"].parent),
                self.directories["magisk"]["remote_path"],
            )
        except Exception as err:
            logger.error(
                f"[{type(err).__name__}] Directory Creation Failed: {err}"
            )
            return None

    def get_dispatcher(self, process_type) -> DispatcherInterface | None:
        from ..variables.functions import set_variable_manager
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
        from ..validation import file_path_validator
        from .functions import parse_file_name

        valid_path = file_path_validator(self.file_path)
        self.data_tuple = VariableTypeTuple(
            file_path=valid_path,
            magisk_image_name="place_holder",
            file_path_stem=Path(valid_path.stem),
            file_parts=parse_file_name(valid_path.stem),
        )
        return self


if __name__ == "__main__":
    path = Path("/path/to/your/file")
    from .functions import set_variable_manager

    variable_manager = set_variable_manager(path)
    print(variable_manager.log_file)
