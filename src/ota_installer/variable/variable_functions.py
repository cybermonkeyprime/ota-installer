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
