# src/ota_installer/program_versioning/software_version.py
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

SoftwareContainer = namedtuple(
    "SoftwareContainer",
    ["title", "major_number", "minor_number", "patch_number"],
)


class SoftwareVersionConstants(Enum):
    """Enumeration for software version constants."""

    TITLE = "OTA-Installer"
    MAJOR_NUMBER = 2025
    MINOR_NUMBER = 12
    PATCH_NUMBER = 19


@dataclass
class SoftwareVersion(object):
    """Data class representing a software version."""

    @property
    def data(self):
        return [enum_member.value for enum_member in SoftwareVersionConstants]

    @property
    def sub_title(self):
        sc = SoftwareContainer(*self.data)
        return f"Build: {sc.major_number}.{sc.minor_number}.{sc.patch_number}"
