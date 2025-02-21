from dataclasses import dataclass, field
from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class DirectoryTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "stock": self.obj.directory.boot_image.stock,  # stock_path
            "magisk": self.obj.directory.boot_image.magisk,  # magisk_path
            "local": self.obj.directory.magisk_image.local_path,
            "remote": self.obj.directory.magisk_image.remote_path,
        }
