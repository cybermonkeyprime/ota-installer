from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from build.components.boot_image.variables import BootImageVariableManager
from build.components.directory.types import (
    DirectoryTypeDefinition,
    DirectoryTypeManager,
)
from build.components.file.variables import FileNameVariableManager
from build.components.log_file import LogFileManager
from build.components.magisk_image.variables import MagiskImageVariableManager
from build.dispatchers import DispatcherManager as MainDispatcher
from build.variables.managers import (
    DispatcherManager,
)


@dataclass
class VariableManager(object):
    """Manages variables related to boot images and file operations."""

    file_path: Path = field(default_factory=Path)

    @property
    def file_name(self) -> FileNameVariableManager:
        return FileNameVariableManager(path=self.file_path)

    @property
    def boot_image(self) -> BootImageVariableManager:
        return BootImageVariableManager(file_path=self.file_name.validator())

    @property
    def patched_image_name(self) -> str:
        magisk_image_variable_manager = MagiskImageVariableManager()
        return magisk_image_variable_manager.image_name

    @patched_image_name.setter
    def patched_image_name(self, image_name: str) -> bool:
        self.patched_image_name = image_name
        return True

    @property
    def log_file(self) -> LogFileManager:
        return LogFileManager(parser=self.file_name.parser())

    @property
    def directory(self) -> Optional[DirectoryTypeDefinition]:
        directory_manager = DirectoryTypeManager(Path.home())
        return directory_manager.create_directory()

    def get_dispatcher(self, object_type: str) -> Optional[MainDispatcher]:
        dispatcher_manager = DispatcherManager(
            dispatcher_class=VariableManager, base_path=self.file_path
        )
        return dispatcher_manager.creator(object_type)


if __name__ == "__main__":
    path = Path("/path/to/your/file")
    variable_manager = VariableManager(file_path=path)
    print(variable_manager.log_file)
