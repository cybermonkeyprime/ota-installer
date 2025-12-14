# src/directories/constants/magisk_paths.py
from collections import namedtuple
from enum import Enum
from pathlib import Path


class MagiskImagePaths(Enum):
    LOCAL_PATH = Path.home() / "Android" / "boot-images" / "magisk"
    REMOTE_PATH = Path("/sdcard") / "Download" / "magisk"


MagiskImageTuple = namedtuple(
    "MagiskImageStruct", ["local_path", "remote_path"]
)
