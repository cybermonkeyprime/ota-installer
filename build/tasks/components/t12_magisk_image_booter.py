from dataclasses import dataclass, field
from pathlib import Path

import build.dispatchers as dispatchers
import build.tasks as tasks
import build.variables as variables


@dataclass
class MagiskImageBooter(tasks.TaskFactoryTemplate):
    instance: type = field(default=variables.Manager)

    def __post_init__(self) -> None:
        try:
            magisk = self.instance.boot_image_struct.magisk
            device = self.instance.file_name_parser.device

            self.index: int = 4
            self.title: str = "Boot to Magisk Image"
            self.path: str = str(
                Path.home().joinpath(magisk.directory_path, magisk.file_name)
            )
            self.command_string: str = (
                f"fastboot flash {self._image_handler(device)} {self.path}"
            )
        except AttributeError as e:
            raise ValueError("Invalid instance attribute") from e

    def _image_handler(self, key: str) -> dispatchers.DispatcherTemplate:
        try:
            dispatcher = dispatchers.MainDispatcher("image")
            retriever = dispatcher.get_dispatcher()
            return retriever.get_key(key)
        except AttributeError as e:
            raise ValueError("Invalid key for image handler") from e
