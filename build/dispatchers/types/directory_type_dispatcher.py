from dataclasses import dataclass, field
from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class DirectoryTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "stock": self.obj.directory.boot_image_path.stock,
            "magisk": self.obj.directory.boot_image_path.magisk,
            "local": self.obj.directory.magisk_image_path.local_path,
            "remote": self.obj.directory.magisk_image_path.remote_path,
        }
