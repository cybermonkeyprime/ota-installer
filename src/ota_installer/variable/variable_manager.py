# src/ota_installer/variables/variable_manager.py
from dataclasses import asdict, dataclass, field
from pathlib import Path

from ..directory.directory_info import DirectoryConfig, set_directory
from ..dispatcher.dispatcher_info import DispatcherType
from ..image.generic_image_info import FileImageData, FileImageNames
from ..image.magisk_image_info import MagiskImagePath
from ..variable.variable_functions import (
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
        from ..image.boot_image_info import BootImageContainer

        self.variables = VariableType.CONTEXT.build(
            file_path=self.path,
            magisk_image_name="place_holder",
            file_path_stem=self.path.stem,
            file_parts=parse_file_name(raw_name=self.path),
        )
        if self.variables:
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
                stock=image_data(FileImageNames.STOCK),
                magisk=image_data(FileImageNames.MAGISK),
                payload=image_data(FileImageNames.PAYLOAD),
                log_file=set_log_file(self.file_name.parts),
            )

            self.ota_parent_directory = self.path.parent
            self.directory = set_directory(self.file_name.path.parent)

            self.boot_directories = BootImageContainer.create()
            self.directories = VariableType.DIRECTORY.build(
                magisk=DirectoryPaths(
                    local_path=MagiskImagePath.LOCAL_PATH.value,
                    remote_path=MagiskImagePath.REMOTE_PATH.value,
                ),
            )
            self.image_name = {
                "patched": self.variables.magisk_image_name,
            }
            # self.set_api_adapter()

    def set_api_adapter(self) -> dict:
        from pprint import pprint

        variable_api = {
            "files_paths": asdict(self.file_paths),
            "directory_paths": {
                "parent": self.ota_parent_directory,
                "boot_paths": asdict(self.boot_directories),
            }
            | asdict(self.directories),
        }
        pprint(variable_api)
        return variable_api

    def get_dispatcher(self, process_type) -> type | None:
        """Retrieves the dispatcher for the given process type."""
        return DispatcherType.get_dispatcher(process_type, self)


# Signed off by Brian Sanford on 20260629
