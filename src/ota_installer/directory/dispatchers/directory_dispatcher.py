# src/ota_installer/directory/dispatchers/directory_dispatcher.py
from dataclasses import dataclass, field

from ...dispatchers.templates import DispatcherTemplate
from ..constants.directory_constants import DirectoryConstants as directory


@dataclass
class DirectoryDispatcher(DispatcherTemplate):
    obj: type = field(default_factory=lambda: type)

    def __post_init__(self) -> None:
        boot_image = self.obj.directory.boot_image
        self.collection = {
            directory.STOCK.value: boot_image.stock,  # stock_path
            directory.MAGISK.value: boot_image.magisk,  # magisk_path
            directory.LOCAL.value: self.obj.directories["magisk"][
                "local_path"
            ],
            directory.REMOTE.value: self.obj.directories["magisk"][
                "remote_path"
            ],
        }
