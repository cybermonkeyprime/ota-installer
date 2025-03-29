from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import build.dispatchers as dispatchers
import build.structures as structures
import build.types.definitions as type_definitions
import build.types.managers as type_managers
import build.variables.managers as variable_managers

magisk = structures.MagiskStruct()


@dataclass
class VariableManager(object):
    """Manages variables related to boot images and file operations."""

    file_path: Path = field(default_factory=Path)

    @property
    def file_name(self) -> "variable_managers.FileNameManager":
        return variable_managers.FileNameManager(path=self.file_path)

    def file_name_manager(self) -> "variable_managers.FileNameManager":
        return variable_managers.FileNameManager(path=self.file_path)

    @property
    def boot_image(self) -> "variable_managers.BootImageManager":
        return variable_managers.BootImageManager(file_path=self.file_name.validator())

    @property
    def patched_image_name(self) -> str:
        patched_image_manager = variable_managers.PatchedImageManager()
        return patched_image_manager.image_name

    @patched_image_name.setter
    def patched_image_name(self, image_name: str) -> bool:
        patched_image_creator = variable_managers.PatchedImageManager(
            image_name=image_name
        )
        self.patched_image_name = patched_image_creator.image_name
        return True

    @property
    def log_file(self) -> "variable_managers.LogFileManager":
        return variable_managers.LogFileManager(parser=self.file_name.parser())

    @property
    def directory(self) -> Optional[type_definitions.Directory]:
        directory_manager = type_managers.Directory(self.file_name.path.parent)
        return directory_manager.create_directory()

    def get_dispatcher(self, object_type: str) -> Optional[dispatchers.MainDispatcher]:
        dispatcher_manager = variable_managers.DispatcherManager(
            dispatcher_class=VariableManager, base_path=self.file_path
        )
        return dispatcher_manager.creator(object_type)


if __name__ == "__main__":
    path = Path("/path/to/your/file")
    variable_manager = VariableManager(file_path=path)
    print(variable_manager.log_file)
