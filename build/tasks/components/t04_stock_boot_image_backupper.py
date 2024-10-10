from dataclasses import dataclass, field
from pathlib import Path

import build.dispatchers as dispatchers
import build.tasks as tasks
import build.variables as variables


@dataclass
class StockBootImageBackupper(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        stock = self.instance.boot_image_struct.stock
        device = self.instance.file_name_parser.device

        self.index: int = 4
        self.title: str = "Backup Stock Boot Image"

        source: str = str(
            Path.home().joinpath("images", f"{self._image_handler(device)}.img")
        )
        destination: str = str(
            Path.home().joinpath(stock.directory_path, stock.file_name)
        )

        self.command_string: str = f"cp -v {source} {destination}"

    def _image_handler(self, key: str) -> dispatchers.DispatcherTemplate:
        try:
            dispatcher = dispatchers.MainDispatcher("image")
            retriever = dispatcher.get_dispatcher()
            return retriever.get_key(key)
        except KeyError as e:
            raise ValueError(f"Invalid key for image handler: {key}") from e
