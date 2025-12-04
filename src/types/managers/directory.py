# src/types/managers/directory.py
from dataclasses import dataclass, field
from pathlib import Path

# import src.types.definitions as definitions
import src.components.directory.types.definitions as definitions


@dataclass
class Directory(object):
    parent_directory: Path
    stock_directory: Path = field(
        default=Path.home() / "Android" / "boot-images"
    )
    magisk_directory: Path = field(
        default=Path.home() / "sdcard" / "Download" / "magisk"
    )

    def create_directory(self) -> definitions.DefaultTypeDefinition | None:
        try:
            return definitions.DefaultTypeDefinition(
                self.parent_directory,
                self.stock_directory,
                self.magisk_directory,
            )
        except Exception as e:
            print(f"{self} Error: {e}")
            return None
