# src/ota_installer/program_versioning/containers/software_container.py
from typing import NamedTuple


class SoftwareContainer(NamedTuple):
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int


# Signed off by Brian Sanford on 20260118
