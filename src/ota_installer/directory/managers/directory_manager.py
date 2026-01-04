# src/ota_installer/types/directory/default_type_manager.py
from dataclasses import dataclass
from pathlib import Path

from ...images.boot_image.constants.boot_image_paths import (
    BootImagePaths,
)
from ...log_setup import logger
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
