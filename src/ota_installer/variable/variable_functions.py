# src/ota_installer/handler/variable_handler.py
from pathlib import Path

from ..variable.variable_info import FileNameContainer

StrPathDict = dict[str, Path | str]


def parse_file_name(raw_name: Path) -> FileNameContainer:
    """Parse the raw file name into its components."""

    build_structure: list[str] = raw_name.stem.split(sep="-")
    device, pkg_type, build_id, *signature = build_structure
    return FileNameContainer(
        device=device,
        pkg_type=pkg_type,
        build_id=build_id,
        signature="".join(signature),
    )


def is_base_global(build_id: str) -> bool:
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
        logger.error(f"Invalid file path: {path}. Aborting.")
        raise SystemExit()

    return VariableManager(path=valid_path)
