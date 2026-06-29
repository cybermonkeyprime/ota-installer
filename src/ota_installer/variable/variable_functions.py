# src/ota_installer/handler/variable_handler.py
from pathlib import Path

from ..variable.variable_info import FileNameContainer

StrPathDict = dict[str, Path | str]


def parse_file_name(raw_name: Path) -> FileNameContainer:
    """Parse the raw file name into its components."""

    device, pkg_type, build_id, *signature = raw_name.stem.split(sep="-")
    return FileNameContainer(
        device=device,
        pkg_type=pkg_type,
        build_id=build_id,
        signature="".join(signature),
    )


def is_base_global(build_id: str) -> bool:
    """Check if the build ID is base global."""
    return not any(char.isalpha() for char in build_id.split(".")[-1])


def set_log_file(file_name_parts: FileNameContainer) -> str:
    """Generate a log file path based on device and version."""
    device = file_name_parts.device
    version = file_name_parts.build_id
    return f"/tmp/ota-installer_{device}_{version}.txt"


def set_variable_manager(path: Path) -> "VariableManager":
    from ..log_setup import logger
    from ..validation.ota_package_validator import validate_ota_package
    from ..variable.variable_manager import VariableManager

    """Create a VariableManager instance after validating the file path. """

    valid_path = validate_ota_package(path)

    if not valid_path:
        message = f"Invalid file path: {path}. Aborting."
        logger.error(message)
        raise FileNotFoundError(message)

    return VariableManager(path=valid_path)


# Signed off by Brian Sanford on 20260629
