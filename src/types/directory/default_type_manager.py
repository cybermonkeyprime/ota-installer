# src/types/directory/default_type_manager.py
from dataclasses import dataclass
from pathlib import Path

import src.types.directory as directory
from src.logger import logger
from src.paths.constants import BootImagePaths


@dataclass
class DefaultTypeManager(object):
    parent_directory: Path

    def create_directory(self) -> directory.DefaultTypeDefinition | None:
        # print("Creating Directories")
        try:
            return directory.DefaultTypeDefinition(
                self.parent_directory,
                str(BootImagePaths.STOCK.value),
                BootImagePaths.MAGISK.value,
            )
        except Exception as err:
            logger.exception(f"{type(err).__name__}: {err}")
            return None
