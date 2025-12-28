# src/ota_installer/variables/functions.py
from collections.abc import Callable
from pathlib import Path


def set_log_file(file_name_parts: Callable) -> str:
    device = file_name_parts.device
    version = file_name_parts.version
    return f"/tmp/ota_variables_{device}_{version}.txt"


def parse_file_name(path):
    from ..structures.file_name_parser import FileNameParser

    return FileNameParser(path)  # .set_raw_name(path).parse_file_name())


def set_variable_manager(path: Path) -> "VariableManager":  # noqa: F821 # pyright: ignore[reportUndefinedVariable]
    from ..variables import VariableManager

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
