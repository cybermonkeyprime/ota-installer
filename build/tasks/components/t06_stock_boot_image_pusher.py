from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
import build.variables as variables


@dataclass
class StockBootImagePusher(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)
    comment_string: str = field(default="Patch boot image in Magisk app")

    @property
    def index(self) -> int:
        return 2

    @property
    def title(self) -> str:
        return "Push Stock Boot Image"

    @property
    def command_string(self) -> str:
        stock = self.instance.boot_image_struct.stock
        return (
            f"adb push {Path.home() / stock.directory_path / stock.file_name} /sdcard/"
        )
