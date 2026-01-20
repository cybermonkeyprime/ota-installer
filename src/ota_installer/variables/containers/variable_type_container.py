# src/ota_installer/variables/containers/variable_type_container.py
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class VariableTypeContainer(object):
    """Container for variable types used in OTA installation."""

    file_path: Path
    magisk_image_name: str
    file_path_stem: str
    file_parts: list[str]


# Signed off by Brian Sanford on 20260120
