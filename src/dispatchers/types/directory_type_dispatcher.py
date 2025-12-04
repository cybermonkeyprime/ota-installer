from dataclasses import dataclass, field

from ..mappings import DirectoryTypeMapping
from ..templates import DispatcherTemplate


@dataclass
class DirectoryTypeDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        boot_image = self.obj.directory.boot_image
        magisk_image = self.obj.directory.magisk_image
        dt = DirectoryTypeMapping
        self.collection = {
            dt.STOCK.value: boot_image.stock,  # stock_path
            dt.MAGISK.value: boot_image.magisk,  # magisk_path
            dt.LOCAL.value: magisk_image.local_path,
            dt.REMOTE.value: magisk_image.remote_path,
        }
