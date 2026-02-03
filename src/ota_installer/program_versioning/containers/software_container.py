# src/ota_installer/program_versioning/containers/software_container.py
from dataclasses import dataclass


@dataclass
class SoftwareContainer(object):
    """Represents a software container with versioning information."""

    title: str
    major_number: int
    minor_number: int
    patch_number: int


# Signed off by Brian Sanford on 20260203
