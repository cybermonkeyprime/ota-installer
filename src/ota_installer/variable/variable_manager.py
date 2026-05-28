# src/ota_installer/variables/variable_manager.py
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..dispatcher.dispatcher_info import DispatcherType
from ..handler.directory_handler import (
    DirectoryDefinition,
    set_directory,
)
from ..handler.image.magisk_image_handler import MagiskImagePath
from ..handler.variable_handler import (
    get_file_image_path,
    parse_file_name,
    set_log_file,
    set_variable_manager,
)
from ..log_setup import logger
from .variable_info import (
    DirectoryNames,
    DirectoryPaths,
    FileNameInfo,
    FilePaths,
    VariableTypeContainer,
)


@dataclass
class VariableManager:
    """Manages variables for OTA installation."""

    path: Path = field(default_factory=Path)

    """ directory type validation"""
    directory: DirectoryDefinition | None = field(init=False)

    """dicts"""
    file_paths: FilePaths = field(init=False)
    file_name: FileNameInfo = field(init=False)
    image_name: dict[str, str] = field(default_factory=dict, init=False)
    directories: DirectoryNames = field(init=False)

    def __post_init__(self) -> None:
        self.variables: VariableTypeContainer = (
            self._initialize_variable_group(file_path=self.path)
        )
        self._initialize_file_name_attributes()
        self._initialize_file_paths()
        self._initialize_directory_paths()
        self._initialize_image_names()

    def _initialize_variable_group(
        self, file_path: Path
    ) -> VariableTypeContainer:
        """Defines variables based on the file path."""
        return VariableTypeContainer(
            file_path=file_path,
            magisk_image_name="place_holder",
            file_path_stem=file_path.stem,
            file_parts=parse_file_name(raw_name=file_path),
        )

    def _initialize_file_name_attributes(self) -> Self:
        """Initializes file name attributes."""
        self.file_name = FileNameInfo(
            path=self.variables.file_path,
            stem=self.variables.file_path_stem,
            parts=self.variables.file_parts,
            device=self.variables.file_parts.device,
            version=self.variables.file_parts.build_id,
        )
        return self

    def _initialize_file_paths(self) -> Self:
        """Initializes file paths."""
        from ..handler.image.generic_image_handler import (
            FileImageData,
        )

        image_data = FileImageData(
            self.file_name.device, self.file_name.version
        )
        self.file_paths = FilePaths(
            stock=get_file_image_path("stock", *image_data),
            magisk=get_file_image_path("magisk", *image_data),
            payload=get_file_image_path("payload", *image_data),
            log_file=set_log_file(self.file_name.parts),
        )
        return self

    def _initialize_directory_paths(self) -> Self:
        """Initializes directory paths."""
        self.ota_parent_directory = self.path.parent
        self.directory = set_directory(self.file_name.path.parent)

        self.directories = DirectoryNames(
            magisk=DirectoryPaths(
                local_path=MagiskImagePath.LOCAL_PATH.value,
                remote_path=MagiskImagePath.REMOTE_PATH.value,
            )
        )
        return self

    def _initialize_image_names(self) -> Self:
        """Initializes image names."""
        self.image_name = {
            "patched": self.variables.magisk_image_name,
        }

        return self

    def create_directory(self) -> DirectoryDefinition | None:
        """Creates a directory and returns its definition."""
        return DirectoryDefinition(
            self.path.parent,
            str(self.file_paths.stock.parent),
            self.directories.magisk.remote_path,
        )

    def get_dispatcher(self, process_type) -> type | None:
        """Retrieves the dispatcher for the given process type."""
        function_call = set_variable_manager(self.path)
        logger.debug("VariableManager.get_dispatcher(): function_call)")
        return DispatcherType.retrieve_dispatcher(process_type, function_call)


def main():
    """Main function to initialize VariableManager and print log_file."""
    path = Path("/path/to/your/file")

    variable_manager = set_variable_manager(path)
    print(variable_manager.file_paths.log_file)


if __name__ == "__main__":
    main()
