# src/ota_installer/variables/functions.py
from collections.abc import Callable
from pathlib import Path

from ota_installer.variables.containers.file_name_container import (
    FileNameContainer,
)


def set_log_file(file_name_parts: Callable) -> str:
    device = file_name_parts.device
    version = file_name_parts.version
    return f"/tmp/ota-installer_{device}_{version}.txt"


def set_variable_manager(path: Path) -> "VariableManager":  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    import sys

    from ..log_setup import logger
    from ..validation.file_path_validation import file_path_validator
    from .variable_manager import VariableManager

    """Create a VariableManager instance after validating the file path. """

    valid_path = file_path_validator(path)
    if not valid_path:
        logger.error(f"Invalid file path: {path}")
        sys.exit("Invalid input file. Aborting.")

    return VariableManager(path)


def get_file_image_path(name: str, device: str, version) -> Path:
    from ..images.file_image.constants.file_image_attributes import (
        FileImageAttributes,
    )

    """Retrieve the file image path based on name, device, and version. """

    return (
        FileImageAttributes[name.upper()]
        .set_device(device)
        .set_version(version)
        .set_file_path()
    )


def parse_file_name(raw_name: Path) -> "FileNameContainer":
    from .containers.file_name_container import FileNameContainer

    """Parse the raw file name into its components. """

    parts = Path(raw_name).stem.split("-")
    device, file_type, version, *extra_parts = parts
    return FileNameContainer(
        device=device,
        file_type=file_type,
        version=version,
        extra=extra_parts,
    )


# Signed off by Brian Sanford on 20260120
