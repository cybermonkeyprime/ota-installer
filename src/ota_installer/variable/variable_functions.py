# src/ota_installer/variable/variable_functions.py
from pathlib import Path

from ..variable.variable_info import FileNameRenderer

StrPathDict = dict[str, Path | str]


def get_file_parts(raw_name: Path) -> FileNameRenderer:
    """Parse the raw file name into its components."""

    device, pkg_type, build_id, *signature = raw_name.stem.split(sep="-")
    return FileNameRenderer(
        device=device,
        pkg_type=pkg_type,
        build_id=build_id,
        signature="".join(signature),
    )


def set_variable_director(path: Path) -> "VariableDirector":
    from ..log_setup import logger
    from ..validation.ota_package_validator import validate_ota_package
    from ..variable.variable_director import VariableDirector

    """Create a VariableDirector instance after validating the file path. """

    valid_path = validate_ota_package(path)

    if not valid_path:
        message = f"Invalid file path: {path}. Aborting."
        logger.error(message)
        raise FileNotFoundError(message)

    return VariableDirector(path=valid_path)


# Signed off by Brian Sanford on 20260629
