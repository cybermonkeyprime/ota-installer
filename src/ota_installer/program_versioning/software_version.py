# src/ota_installer/program_versioning/software_version.py
from dataclasses import dataclass

from .constants.software_constants import SoftwareConstants
from .containers.software_container import SoftwareContainer


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    @property
    def data(self):
        return [enum_member.value for enum_member in SoftwareConstants]

    @property
    def display(self):
        sc = SoftwareContainer(*self.data)
        return f"Build: {sc.major_number}.{sc.minor_number}.{sc.patch_number}"
