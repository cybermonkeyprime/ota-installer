from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class MagiskDirectories(Enum):
    LOCAL = Path.home() / "Android" / "boot-images" / "magisk"
    REMOTE = Path("/sdcard") / "Download" / "magisk"


@dataclass
class Magisk(object):
    local_path: Path = field(
        default_factory=lambda: MagiskDirectories.LOCAL.value
    )
    remote_path: Path = field(
        default_factory=lambda: MagiskDirectories.REMOTE.value
    )


@dataclass
class MagiskStruct(object):
    local_path: Path = field(
        default_factory=lambda: MagiskDirectories.LOCAL.value
    )
    remote_path: Path = field(
        default_factory=lambda: MagiskDirectories.REMOTE.value
    )
