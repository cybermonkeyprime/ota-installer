from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
import build.variables as variables


@dataclass
class PayloadImageExtractor(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        self.index: int = 1
        self.title: str = "Payload Image Extracter"
        self.command_string: str = (
            f"unzip -o {
                self.instance.path} payload.bin -d {Path.home()}"
        )
