from dataclasses import dataclass, field
from pathlib import Path


from dispatchers import MainDispatcher, DispatcherTemplate

import build.tasks as tasks
import build.variables as variables


@dataclass
class BootImageExtractor(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        self.index: int = 3
        self.title: str = "Boot Image Extractor"

        device: str = self.instance.file_name_parser.device
        source: Path = Path.home() / self.instance.boot_image_struct.payload.file_name
        options: str = (
            f"--images={self._image_handler(device)} --out {Path.home() / "images"}"
        )
        self.command_string: str = f"payload_dumper.py {source} {options}"

    def _image_handler(self, key: str) -> DispatcherTemplate:
        try:
            dispatcher = MainDispatcher("image")
            retriever = dispatcher.get_dispatcher()
            return retriever.get_key(key)
        except KeyError as e:
            raise ValueError(f"Invalid key for image handler: {key}") from e
