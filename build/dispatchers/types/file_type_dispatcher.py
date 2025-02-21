from dataclasses import dataclass, field
from typing import Any

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class FileTypeDispatcher(DispatcherTemplate):
    obj: Any = field(default_factory=lambda: "")

    def __post_init__(self) -> None:
        self.collection = {
            "payload": self.obj.boot_image_struct.payload,
            "stock": self.obj.boot_image_struct.stock,
            "magisk": self.obj.boot_image_struct.magisk,
        }
