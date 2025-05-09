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
from build.dispatchers import DispatcherManager as MainDispatcher
from build.variables.managers import (
    DispatcherManager,
)


@dataclass
class VariableManager(object):
    """Manages variables related to boot images and file operations."""

    file_path: Path = field(default_factory=Path)
    patched_image_name: str = field(default="placeholder")

    @property
    def file_name(self) -> FileNameVariableManager:
        return FileNameVariableManager(path=self.file_path)

    @property
    def boot_image(self) -> BootImageVariableManager:
        return BootImageVariableManager(file_path=self.file_name.validator())

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
