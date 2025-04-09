from dataclasses import dataclass, field
from pathlib import Path


from build.dispatchers import DispatcherManager, DispatcherTemplate

import build.tasks as tasks
import build.variables as variables


@dataclass
class BootImageExtractor(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 3

    @property
    def title(self) -> str:
        return "Boot Image Extractor"

    @property
    def command_string(self) -> str:
        device: str = self.instance.file_name.parts.device
        source: Path = Path.home() / self.instance.boot_image.struct.payload.file_name
        options: str = (
            f"--images={self._image_handler(device)} --out {Path.home() / 'images'}"
        )
        return f"payload_dumper {source} {options}"

    def _image_handler(self, key: str) -> DispatcherTemplate:
        try:
            dispatcher = DispatcherManager("image")
            retriever = dispatcher.get_dispatcher()
            return retriever.get_key(key)
        except KeyError as e:
            raise ValueError(f"Invalid key for image handler: {key}") from e
