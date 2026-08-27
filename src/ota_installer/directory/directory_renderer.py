from enum import Enum

from ..log_setup import logger


class DirectoryRender(Enum):
    from ..image.boot_image_info import BootImageContainer
    from ..image.magisk_image_info import MagiskImageContainer

    BOOT = BootImageContainer.create
    MAGISK = MagiskImageContainer

    def __call__(self, *args, **kwargs):
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating directory container: {self.name}")
        return self.value(*args) if args else None
