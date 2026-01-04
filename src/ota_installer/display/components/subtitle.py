# src/ota_installer/display/components/subtitle.py

from ...decorators.colorizer import Colorizer
from ...program_versioning.software_version import SoftwareVersion


@Colorizer(style="version")
def display_subtitle() -> str:
    sv = SoftwareVersion()
    """
    String representation of the DisplaySubtitle instance.
    """

    return sv.display
