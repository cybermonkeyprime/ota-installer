from dataclasses import dataclass, field
from pathlib import Path

import build.tasks as tasks
import build.variables as variables


@dataclass
class StockBootImagePusher(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        stock = self.instance.boot_image_struct.stock
        self.index: int = 2
        self.title: str = "Push Stock Boot Image"
        self.command_string: str = (
            f"adb push {Path.home() / stock.directory_path / stock.file_name} /sdcard/"
        )
        self.comment = "Patch boot image in Magisk app"
