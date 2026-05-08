# src/ota_installer/variables/functions.py
from pathlib import Path

from ota_installer.variables.containers.file_name_container import (
    FileNameContainer,
)


def set_log_file(file_name_parts: FileNameContainer) -> str:
    """Generate a log file path based on device and version."""
    device = file_name_parts.device
    version = file_name_parts.build_id
    return f"/tmp/ota-installer_{device}_{version}.txt"


def set_variable_manager(path: Path) -> "VariableManager":  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    from ..log_setup import logger
    from ..validation.validate_zip_file import validate_zip_file
    from .variable_manager import VariableManager

    """Create a VariableManager instance after validating the file path. """

    valid_path = validate_zip_file(path)

    if not valid_path:
        logger.error(f"Invalid file path: {path}. Aborting.")
        raise SystemExit()

    return VariableManager(valid_path)


def get_file_image_path(name: str, device: str, version) -> Path:
    from ..images.generic_image_handler import (
        FileImageAttributes,
    )

    """Retrieve the file image path based on name, device, and version. """

    return (
        FileImageAttributes[name.upper()]
        .set_device(device)
        .set_version(version)
        .set_file_path()
    )
