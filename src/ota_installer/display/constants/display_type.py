# src/ota_installer/display/constants/display_type.py
from enum import Enum

from ...program_versioning.constants.software_constants import SoftwareType


class DisplayType(Enum):
    VERBOSE = SoftwareType.render_display()
    CONCISE = SoftwareType.render_text()
