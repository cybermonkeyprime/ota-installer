# src/ota_installer/program_versioning/software_version.py
from enum import Enum

from .constants.software_constants import SoftwareType


class DisplayType(Enum):
    VERBOSE = SoftwareType.render_display()
    CONCISE = SoftwareType.render_text()
