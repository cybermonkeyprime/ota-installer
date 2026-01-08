# src/ota_installer/variables/variable_manager.py
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..directory.definitions.directory_type_definition import (
    DirectoryTypeDefinition,
)
from ..directory.managers.directory_type_manager import set_directory
from ..dispatchers.factories.mappings.dispatcher_factory_mapping import (
    DispatcherTypes,
)
from ..images.magisk_image.constants.magisk_image_paths import (
    MagiskImagePaths,
)
from ..log_setup import logger
from .containers.variable_type_container import VariableTypeContainer
from .functions import set_variable_manager


@dataclass
class VariableManager(object):
    """Manages variables for OTA installation."""

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
        self.variables = define_variable(self.path)  # .data_tuple
        self.define_file_name_attributes()
        self.define_file_paths()
        self.define_directory_paths()
        self.define_image_names()

    def define_file_name_attributes(self) -> Self:
        """Defines file name attributes."""
        self.file_name = {
            "path": self.variables.file_path,
            "stem": self.variables.file_path_stem,
            "parts": self.variables.file_parts,
            "device": self.variables.file_parts.device,
            "version": self.variables.file_parts.version,
        }
        return self

    def define_file_paths(self) -> Self:
        from ..images.file_image.containers.file_image_container import (
            FileImageData,
        )
        from ..variables.functions import (
            get_file_image_path,
            set_log_file,
        )

        """Defines file paths."""
        image_data = FileImageData(
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
        """Defines directory paths."""
        self.ota_parent_directory = self.path.parent
        self.directory = set_directory(self.file_name["path"].parent)

        self.directories = {
            "magisk": {
                "local_path": MagiskImagePaths.LOCAL_PATH.value,
                "remote_path": MagiskImagePaths.REMOTE_PATH.value,
            }
        }
        return self

    def define_image_names(self) -> Self:
        """Defines image names."""
        self.image_name = {
            "patched": self.variables.magisk_image_name,
        }

        return self

    def create_directory(self) -> DirectoryTypeDefinition | None:
        """Creates a directory and returns its definition."""
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

    def get_dispatcher(self, process_type) -> DispatcherTypes | None:
        from ..dispatchers.factories.dispatch_retriever import (
            DispatchRetriever,
        )

        """Retrieves the dispatcher for the given process type."""
        function_call = set_variable_manager(self.path)
        logger.debug("VariableManager.get_dispatcher(): function_call)")
        return (
            DispatchRetriever(process_type)
            .set_function_call(function_call)
            .get_dispatcher()
        )


def define_variable(file_path: Path) -> VariableTypeContainer:
    from .functions import parse_file_name

    """Defines variables based on the file path."""
    data_tuple = VariableTypeContainer(
        file_path=file_path,
        magisk_image_name="place_holder",
        file_path_stem=Path(file_path.stem),
        file_parts=parse_file_name(file_path),
    )
    return data_tuple


def main():
    """Main function to initialize VariableManager and print log_file."""
    path = Path("/path/to/your/file")

    variable_manager = set_variable_manager(path)
    print(variable_manager.file_paths.get("log_file"))


if __name__ == "__main__":
    main()
