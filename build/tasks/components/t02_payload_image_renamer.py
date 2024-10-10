from dataclasses import dataclass, field
from pathlib import Path


import build.tasks as tasks
import build.variables as variables


@dataclass
class PayloadImageRenamer(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        self.index: int = 2
        self.title: str = "Payload Image Renamer"
        source_path: Path = Path.home().joinpath("payload.bin")
        destination_path: Path = Path.home().joinpath(
            self.instance.boot_image_struct.payload.file_name
        )

        self.command_string: str = f"mv -v {source_path} {destination_path}"
