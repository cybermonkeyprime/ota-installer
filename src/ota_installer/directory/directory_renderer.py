# src/ota_installer/directory/directory_renderer.py
from enum import Enum

from ..log_setup import logger


class DirectoryRender(Enum):
    from ..image.boot.boot_image_container import BootImageContainer
    from ..image.magisk.magisk_image_info import MagiskImageContainer

    BOOT = BootImageContainer.create
    MAGISK = MagiskImageContainer

    def __call__(self, *args, **kwargs):
        """Creates an instance of the specified container class."""
        logger.debug(f"Creating directory container: {self.name}")
        return self.value(*args, **kwargs)


# Signed off by Brian Sanford on 20260827
