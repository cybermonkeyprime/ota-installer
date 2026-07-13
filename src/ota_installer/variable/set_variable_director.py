# src/ota_installer/variable/set_variable_director.py
from pathlib import Path


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


# Signed off by Brian Sanford on 20260712
