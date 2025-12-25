# src/ota_installer/program_versioning/containers/software_container.py
from collections import namedtuple

SoftwareContainer = namedtuple(
    "SoftwareContainer",
    ["title", "major_number", "minor_number", "patch_number"],
)
