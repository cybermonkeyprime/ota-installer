# src/ota_installer/variables/variable_manager.py
from dataclasses import dataclass, field
from pathlib import Path

from ..directory.directory_info import DirectoryConfig, set_directory
from ..dispatcher.dispatcher_info import DispatcherType
from ..image.generic_image_handler import (
    FileImageData,
)
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
    VariableRenderer,
    VariableType,
)


@dataclass
class VariableManager:
    """Manages variables for OTA installation."""

    path: Path = field(default_factory=Path)

    """ directory type validation"""
    directory: DirectoryConfig = field(init=False)
    ota_parent_directory: Path = field(init=False)

    """dicts"""
    variables: VariableRenderer = field(init=False)
    file_paths: FilePaths = field(init=False)
    file_name: FileNameInfo = field(init=False)
    image_name: dict[str, str] = field(init=False)
    directories: DirectoryNames = field(init=False)

    def __post_init__(self) -> None:

        self.variables = VariableType.CONTEXT.build(
            file_path=self.path,
            magisk_image_name="place_holder",
            file_path_stem=self.path.stem,
            file_parts=parse_file_name(raw_name=self.path),
        )
        if self.variables is not None:
            self.file_name = VariableType.FILE_NAME.build(
                path=self.variables.file_path,
                stem=self.variables.file_path_stem,
                parts=self.variables.file_parts,
                device=self.variables.file_parts.device,
                version=self.variables.file_parts.build_id,
            )
            image_data = FileImageData(
                self.file_name.device, self.file_name.version
            )
            self.file_paths = VariableType.FILE_PATH.build(
                stock=get_file_image_path("stock", *image_data),
                magisk=get_file_image_path("magisk", *image_data),
                payload=get_file_image_path("payload", *image_data),
                log_file=set_log_file(self.file_name.parts),
            )

            self.ota_parent_directory = self.path.parent
            self.directory = set_directory(self.file_name.path.parent)

            self.directories = VariableType.DIRECTORY.build(
                magisk=DirectoryPaths(
                    local_path=MagiskImagePath.LOCAL_PATH.value,
                    remote_path=MagiskImagePath.REMOTE_PATH.value,
                )
            )
            self.image_name = {
                "patched": self.variables.magisk_image_name,
            }

    def get_dispatcher(self, process_type) -> type | None:
        """Retrieves the dispatcher for the given process type."""
        return DispatcherType.get_dispatcher(process_type, self.path)
