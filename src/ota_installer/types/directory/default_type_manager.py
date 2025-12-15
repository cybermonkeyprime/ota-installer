# src/ota_installer/types/directory/default_type_manager.py
from dataclasses import dataclass
from pathlib import Path

from ...log_setup import logger
from ...paths.constants import BootImagePaths
from ...types.directory import DefaultTypeDefinition


@dataclass
class DefaultTypeManager(object):
    parent_directory: Path

    def create_directory(self) -> DefaultTypeDefinition | None:
        # print("Creating Directories")
        try:
            return DefaultTypeDefinition(
                self.parent_directory,
                str(BootImagePaths.STOCK.value),
                BootImagePaths.MAGISK.value,
            )
        except Exception as err:
            logger.exception(f"{type(err).__name__}: {err}")
            return None
