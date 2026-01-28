# src/ota_installer/variables/containers/file_name_container.py
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FileNameContainer(object):
    """Container for file name components."""

    device: str
    file_type: str
    version: str
    extra: str | None = None


