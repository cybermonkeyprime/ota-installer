# src/ota_installer/variables/functions.py
from collections.abc import Callable
from pathlib import Path


def set_log_file(file_name_parts: Callable) -> str:
    device = file_name_parts.device
    version = file_name_parts.version
    return f"/tmp/ota_variables_{device}_{version}.txt"


def parse_file_name(path):
    from ..structures import FileNameParser

    return FileNameParser(path)  # .set_raw_name(path).parse_file_name())


def set_variable_manager(path: Path) -> "VariableManager":  # type: ignore[return-value]
    from ..variables import VariableManager

    return VariableManager(path)


def get_file_image_path(name: str, device: str, version) -> str:
    from ..paths.constants import ImageFileAttributes

    return (
        ImageFileAttributes[name.upper()]
        .set_device(device)
        .set_version(version)
        .set_file_path()
    )
