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
    """Creates a DirectoryTypeDefinition for the specified parent directory."""
    logger.debug("Creating Directories")
    if not parent_directory.exists() or not parent_directory.is_dir():
        logger.error("Invalid parent directory: %s", parent_directory)
        return None

    return DirectoryTypeDefinition(
        parent_directory,
        str(BootImagePaths.STOCK.value),
        BootImagePaths.MAGISK.value,
    )


# Signed off by Brian Sanford on 20260213
