from dataclasses import dataclass, field
from pathlib import Path

import build.structures as structures
import build.tasks as tasks
import build.variables as variables
from dispatchers import DispatcherTemplate, MainDispatcher


@dataclass
class StockBootImageBackupper(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 4

    @property
    def title(self) -> str:
        return "Backup Stock Boot Image"

    @property
    def stock_image(self) -> structures.ImageFile:
        return self.instance.boot_image.struct.stock

    @property
    def device_name(self) -> str:
        return self.instance.file_name.parts.device

    @property
    def source_path(self) -> Path:
        return Path.home().joinpath(
            "images", f"{self._image_handler(self.device_name)}.img"
        )

    @property
    def destination_path(self) -> Path:
        return Path.home().joinpath(
            self.stock_image.directory_path, self.stock_image.file_name
        )

    @property
    def command_string(self) -> str:
        return f"cp -v {self.source_path} {self.destination_path}"

    def _image_handler(self, key: str) -> DispatcherTemplate | None:
        try:
            dispatcher = MainDispatcher("image")
            retriever = dispatcher.receiver()
            return retriever.get_key(key)
        except KeyError as e:
            print(f"Invalid key for image handler: {key} from {e}")
            # raise ValueError(f"Invalid key for image handler: {key}") from e
