from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks


@dataclass
class MagiskImagePuller(tasks.TaskFactoryTemplate):
    instance: type = field()

    @property
    def index(self) -> int:
        return 4

    @property
    def title(self) -> str:
        return "Pull Magisk Image:"

    @property
    def magisk_struct(self) -> type:
        return self.instance.boot_image.struct.magisk

    @property
    def magisk_directory(self) -> type:
        return self.instance.directory.magisk_image

    @property
    def magisk_local_path(self) -> Path:
        return Path(self.magisk_directory.local_path)

    @property
    def magisk_remote_path(self) -> Path:
        return Path(self.magisk_directory.remote_path)

    @property
    def source_path(self) -> Path:
        return Path(self.magisk_remote_path) / self.instance.patched_image_name

    @property
    def destination_path(self) -> Path:
        return Path.home() / self.magisk_local_path / self.magisk_struct.file_name

    @property
    def command_string(self) -> str:
        return f"adb pull {self.source_path} {self.destination_path}"
