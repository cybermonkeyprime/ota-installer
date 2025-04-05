from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from build.components.directory.types import DirectoryTypeDefinition


@dataclass
class DirectoryTypeManager(object):
    parent_directory: Path
    stock_directory: str = field(default="Android/boot-images")
    magisk_directory: str = field(default="/sdcard/Download/magisk")

    def create_directory(self) -> Optional[DirectoryTypeDefinition]:
        try:
            return DirectoryTypeDefinition(
                self.parent_directory,
                self.stock_directory,
                self.magisk_directory,
            )
        except Exception as e:
            print(f"{e}")
            return None
