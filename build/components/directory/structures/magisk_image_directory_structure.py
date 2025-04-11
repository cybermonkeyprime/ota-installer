from dataclasses import dataclass, field
from pathlib import Path

from build.components.directory.structures import BootImageDirectoryStructure

@dataclass
class MagiskImageDirectoryStructure:
    """
    A class to represent the structure of Magisk directories.

    Attributes:
        local_path (Path): The local path to the Magisk boot images.
        remote_path (Path): The remote path to the Magisk directory on the device.
    """

    local_path: Path = field(
        default_factory=lambda: BootImageDirectoryStructure().magisk
    )
    remote_path: Path = field(default_factory=lambda: Path("/sdcard/Download/magisk"))
