# src/ota_installer/images/magisk_image/containers/magisk.py
from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path

from ..constants.magisk_image_paths import MagiskImagePaths


@dataclass
class MagiskImageStruct(object):
    local_path: Path = field(
        default_factory=lambda: MagiskImagePaths.LOCAL_PATH.value
    )
    remote_path: Path = field(
        default_factory=lambda: MagiskImagePaths.REMOTE_PATH.value
    )


class MagiskStruct(MagiskImageStruct):
    pass


MagiskImageTuple = namedtuple(
    "MagiskImageStruct", ["local_path", "remote_path"]
)
