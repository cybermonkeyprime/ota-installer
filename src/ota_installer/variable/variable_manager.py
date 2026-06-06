# src/ota_installer/variables/variable_manager.py
from dataclasses import dataclass, field
from pathlib import Path

from ..directory.directory_handler import DirectoryConfig
from ..dispatcher.dispatcher_info import DispatcherType
from ..image.magisk_image_handler import MagiskImagePath
from ..variable.variable_functions import (
    get_file_image_path,
    parse_file_name,
    set_log_file,
)
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
    directory: DirectoryConfig = field(init=False)

    """dicts"""
    variables: VariableTypeContainer = field(init=False)
    file_paths: FilePaths = field(init=False)
    file_name: FileNameInfo = field(init=False)
    image_name: dict[str, str] = field(default_factory=dict, init=False)
    directories: DirectoryNames = field(init=False)

    def __post_init__(self) -> None:
        self.variables = self._initialize_variable_group(file_path=self.path)
        if self.variables is not None:
            self.file_name = self._initialize_file_name_attributes()
            self.file_paths = self._initialize_file_paths()
            self.directories = self._initialize_directory_paths()
            self.image_name = self._initialize_image_names()

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

    def _initialize_file_name_attributes(self) -> FileNameInfo:
        """Initializes file name attributes."""
        return FileNameInfo(
            path=self.variables.file_path,
            stem=self.variables.file_path_stem,
            parts=self.variables.file_parts,
            device=self.variables.file_parts.device,
            version=self.variables.file_parts.build_id,
        )

    def _initialize_file_paths(self) -> FilePaths:
        """Initializes file paths."""
        from ..image.generic_image_handler import (
            FileImageData,
        )

        image_data = FileImageData(
            self.file_name.device, self.file_name.version
        )
        return FilePaths(
            stock=get_file_image_path("stock", *image_data),
            magisk=get_file_image_path("magisk", *image_data),
            payload=get_file_image_path("payload", *image_data),
            log_file=set_log_file(self.file_name.parts),
        )

    def _initialize_directory_paths(self) -> DirectoryNames:
        from ..directory.directory_handler import set_directory

        """Initializes directory paths."""
        self.ota_parent_directory = self.path.parent
        self.directory = set_directory(self.file_name.path.parent)

        return DirectoryNames(
            magisk=DirectoryPaths(
                local_path=MagiskImagePath.LOCAL_PATH.value,
                remote_path=MagiskImagePath.REMOTE_PATH.value,
            )
        )

    def _initialize_image_names(self) -> dict[str, str]:
        """Initializes image names."""
        return {
            "patched": self.variables.magisk_image_name,
        }

        return self

    def create_directory(self) -> DirectoryConfig | None:
        """Creates a directory and returns its definition."""
        return DirectoryConfig(
            self.path.parent,
            str(self.file_paths.stock.parent),
            self.directories.magisk.remote_path,
        )

    def get_dispatcher(self, process_type) -> type | None:
        return DispatcherType.get_dispatcher(process_type, self.path)
