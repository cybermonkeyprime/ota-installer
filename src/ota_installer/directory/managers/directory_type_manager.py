# src/ota_installer/types/directory/default_type_manager.py
from pathlib import Path

from ...images.boot_image.constants.boot_image_paths import (
    BootImagePaths,
)
from ...log_setup import logger
from ..definitions.directory_type_definition import DirectoryTypeDefinition


def set_directory(
    parent_directory: Path,
) -> DirectoryTypeDefinition | None:
    logger.debug("Creating Directories")
    try:
        return DirectoryTypeDefinition(
            parent_directory,
            str(BootImagePaths.STOCK.value),
            BootImagePaths.MAGISK.value,
        )
    except Exception as err:
        logger.exception(f"{type(err).__name__}: {err}")
        return None
