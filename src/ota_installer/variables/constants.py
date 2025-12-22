# src/ota_installer/variables/constants.py
from enum import Enum

from ..images.magisk_image.constants.magisk_image_paths import MagiskImagePaths


class DispatcherTypes(Enum):
    DIRECTORY = "directory"
    FILE = "file"
    VARIABLE = "variable"

    def __str__(self) -> str:
        return self.value


class MagiskDirectoryConstants(Enum):
    LOCAL_PATH = MagiskImagePaths.LOCAL_PATH.value
    REMOTE_PATH = MagiskImagePaths.REMOTE_PATH.value
