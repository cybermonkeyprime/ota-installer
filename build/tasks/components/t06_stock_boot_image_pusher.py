from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
import build.variables as variables


@dataclass
class StockBootImagePusher(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)
    comment_string: str = field(default="Patch boot image in Magisk app")

    @property
    def index(self) -> int:
        return 2

    @property
    def title(self) -> str:
        return "Push Stock Boot Image"

    @property
    def stock(self) -> str:
        return self.instance.boot_image.struct.stock

    @property
    def command_string(self) -> str:
        return f"adb push {Path.home() / self.stock.directory_path / self.stock.file_name} /sdcard/"
