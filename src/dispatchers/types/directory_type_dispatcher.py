# src/dispatchers/types/directory_type_dispatcher.py
from dataclasses import dataclass, field

from ..mappings import DirectoryTypeMapping
from ..templates import DispatcherTemplate


@dataclass
class DirectoryTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        boot_image = self.obj.directory.boot_image
        dt = DirectoryTypeMapping
        self.collection = {
            dt.STOCK.value: boot_image.stock,  # stock_path
            dt.MAGISK.value: boot_image.magisk,  # magisk_path
            dt.LOCAL.value: self.obj.magisk_image.local_path,
            dt.REMOTE.value: self.obj.magisk_image_remote_path,
        }
