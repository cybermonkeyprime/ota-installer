# src/ota_installer/display/constants/display_type.py
from enum import Enum

from ...version_handler import SoftwareType


class DisplayType(Enum):
    VERBOSE = SoftwareType.render_display()
    CONCISE = SoftwareType.render_text()
