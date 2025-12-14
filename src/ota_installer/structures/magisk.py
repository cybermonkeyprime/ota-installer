# src/ota_installer/structures/magisk.py
from collections import namedtuple
from dataclasses import dataclass, field
from pathlib import Path

from src.ota_installer.paths.constants import MagiskImagePaths


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
