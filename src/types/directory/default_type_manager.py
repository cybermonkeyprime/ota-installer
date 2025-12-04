from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import src.types.directory as directory
from src.logger import logger


class DefaultTypeDirectories(Enum):
    STOCK = Path.home() / "Android" / "boot-images"
    MAGISK = Path.home() / "sdcard" / "Download" / "magisk"


@dataclass
class DefaultTypeManager(object):
    parent_directory: Path

    def create_directory(self) -> directory.DefaultTypeDefinition | None:
        # print("Creating Directories")
        try:
            return directory.DefaultTypeDefinition(
                self.parent_directory,
                str(DefaultTypeDirectories.STOCK.value),
                DefaultTypeDirectories.MAGISK.value,
            )
        except Exception as err:
            logger.exception(f"{type(err).__name__}: {err}")
            return None
