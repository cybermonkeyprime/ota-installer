from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
import build.variables as variables


@dataclass
class PayloadImageExtractor(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 1

    @property
    def title(self) -> str:
        return "Payload Image Extracter"

    @property
    def command_string(self) -> str:
        return f"unzip -o {self.instance.file_path} payload.bin -d {Path.home()}"
