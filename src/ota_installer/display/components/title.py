# src/ota_installer/display/components/title.py

from ...decorators import StyledFigletPrinter
from ...program_versioning.constants.software_constants import (
    SoftwareConstants,
)


@StyledFigletPrinter(style="title", font="slant")
def display_title() -> str:
    """
    Generate and return a stylized string representation of the application
        title.
    """

    return f" {SoftwareConstants.TITLE.value}"


# Signed off by Brian Sanford on 20260213
