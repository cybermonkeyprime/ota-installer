from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import src.components.directory.types.definitions as dtd


class DefaultTypeDirectories(Enum):
    STOCK = Path.home() / "Android" / "boot-images"
    MAGISK = Path.home() / "sdcard" / "Download" / "magisk"


@dataclass
class DefaultTypeManager(object):
    parent_directory: Path

    def create_directory(self) -> dtd.DefaultTypeDefinition | None:
        # print("Creating Directories")
        try:
            return dtd.DefaultTypeDefinition(
                self.parent_directory,
                DefaultTypeDirectories.STOCK.value,
                DefaultTypeDirectories.MAGISK.value,
            )
        except Exception as e:
            print(f"{e}")
            return None
