from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks


@dataclass
class MagiskImagePuller(tasks.TaskFactoryTemplate):
    instance: type = field()

    def __post_init__(self) -> None:
        magisk = self.instance.boot_image_struct.magisk
        magisk_directory = self.instance.directory.magisk_image

        magisk_local_path = Path(magisk_directory.local_path)
        magisk_remote_path = Path(magisk_directory.remote_path)

        self.index = 4
        self.title = "Pull Magisk Image:"
        self.source_path: Path = (
            Path(magisk_remote_path) / self.instance.patched_image_name
        )
        self.destination_path = Path.home() / magisk_local_path / magisk.file_name
        self.command_string = f"adb pull {self.source_path} {self.destination_path}"
