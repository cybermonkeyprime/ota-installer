from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
from build.dispatchers import DispatcherTemplate, MainDispatcher


@dataclass
class MagiskImageBooter(tasks.TaskFactoryTemplate):
    instance: type = field(default=type)

    @property
    def index(self) -> int:
        return 4

    @property
    def title(self) -> str:
        return "Boot to Magisk Image"

    @property
    def magisk_struct(self) -> type:
        return self.instance.boot_image.struct.magisk

    @property
    def device_name(self) -> str:
        return self.instance.file_name.parser.device

    @property
    def magisk_image_path(self) -> Path:
        return Path.home().joinpath(
            self.magisk_struct.directory_path, self.magisk_struct.file_name
        )

    @property
    def command_string(self) -> str:
        return f"fastboot flash {self._image_handler(self.device_name)} {self.magisk_image_path}"

    def _image_handler(self, key: str) -> DispatcherTemplate:
        try:
            dispatcher = MainDispatcher("image")
            retriever = dispatcher.get_dispatcher()
            return retriever.get_key(key)
        except AttributeError as e:
            raise ValueError("Invalid key for image handler") from e
