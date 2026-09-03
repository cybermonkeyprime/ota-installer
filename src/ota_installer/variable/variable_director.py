# src/ota_installer/variables/variable_director.py
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Self

from loguru import logger

from ..directory.directory_pipeline import set_directory_pipeline
from ..dispatcher.dispatcher_builder import build_dispatcher
from ..image.magisk.magisk_image_info import MagiskImagePath
from .variable_invocations import (
    MagiskPathInvocation,
)
from .variable_renderers import VariableType


@dataclass
class VariableDirector:
    """Manages variables for OTA installation."""

    path: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        self.magisk_image: str = "place_holder"

    def set_base_variables(self) -> Self:
        self.variables = VariableType.CONTEXT.build(file_path=self.path)
        if self.undefined_variables_error():
            message = "Variables are unset or invalid"
            logger.error(message)
            raise AttributeError(message)
        return self

    def undefined_variables_error(self) -> bool:
        return bool(self.variables is None or self.variables == "")

    def set_filenames(self):
        self.file_name = VariableType.FILE_NAME.build(
            path=self.file_path, parts=self.file_parts
        )
        self.file_paths = VariableType.FILE_PATH.build(parts=self.file_parts)
        return self

    def set_directories(self) -> Self:
        from ..image.boot.boot_image_container import BootImageContainer

        self.ota_parent_directory = self.path.parent
        self.directory = set_directory_pipeline(self.file_name.path.parent)

        self.boot_directories = BootImageContainer.create()
        self.directories = VariableType.DIRECTORY.build(
            magisk=MagiskPathInvocation(
                local_path=MagiskImagePath.LOCAL_PATH.value,
                remote_path=MagiskImagePath.REMOTE_PATH.value,
            ),
        )
        self.image_name = {
            "patched": self.file_paths.magisk_image_name,
        }
        return self

    @property
    def file_path(self) -> Path:
        return self.variables.file_path

    @property
    def file_parts(self) -> Path:
        return self.variables.file_parts

    def to_context(self) -> tuple:
        from pprint import pprint

        variable_api = tuple(
            {
                "files_paths": asdict(self.file_paths),
                "directory_paths": {
                    "parent": self.ota_parent_directory,
                    "boot_paths": asdict(self.boot_directories),
                }
                | asdict(self.directories),
            }
        )
        pprint(variable_api)
        return variable_api

    def get_dispatcher(self, process_type) -> object:
        """Retrieves the dispatcher for the given process type."""
        return build_dispatcher(process_type, self)


def variable_pipeline(path: Path) -> VariableDirector:
    from ..log_setup import logger
    from ..validation.ota_package_validator import validate_ota_package
    from ..variable.variable_director import VariableDirector

    """Create a VariableDirector instance after validating the file path. """

    valid_path = validate_ota_package(path)

    if not valid_path:
        message = f"Invalid file path: {path}."
        report = {"status": "Error", "response": message}
        logger.critical(report)
        raise FileNotFoundError(report)

    return (
        VariableDirector(path=valid_path)
        .set_base_variables()
        .set_filenames()
        .set_directories()
    )


# Signed off by Brian Sanford on 20260629
