# src/ota_installer/variables/functions.py
from collections.abc import Callable
from pathlib import Path


def set_log_file(file_name_parts: Callable) -> str:
    device = file_name_parts.device
    version = file_name_parts.version
    return f"/tmp/ota_variables_{device}_{version}.txt"


def set_variable_manager(path: Path) -> "VariableManager":  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    import sys

    from ..log_setup import logger
    from ..validation.file_path_validation import file_path_validator
    from .variable_manager import VariableManager

    valid_path = file_path_validator(path)
    if not valid_path:
        logger.error(f"Invalid file path: {path}")
        sys.exit("Invalid input file. Aborting.")

    return VariableManager(path)


def get_file_image_path(name: str, device: str, version) -> str:
    from ..images.file_image.constants.file_image_attributes import (
        FileImageAttributes,
    )

    return (
        FileImageAttributes[name.upper()]
        .set_device(device)
        .set_version(version)
        .set_file_path()
    )
