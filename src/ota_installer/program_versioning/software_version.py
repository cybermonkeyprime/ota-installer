# src/ota_installer/program_versioning/software_version.py
from dataclasses import dataclass

from .builders.software_container_builder import build_software_container


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    @property
    def display(self):
        sc = build_software_container()
        return f"Build: {sc.major_number}.{sc.minor_number}.{sc.patch_number}"
