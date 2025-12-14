# src/ota_installer/display/components/subtitle.py

from dataclasses import dataclass

import src.ota_installer.decorators.colorizer as colorizer
import src.ota_installer.display.templates as display_templates
import src.ota_installer.program_versioning.software_version as software_version


@dataclass
class Subtitle(display_templates.DisplayComponent):
    """
    Subtitle class that inherits from DisplayComponent and is responsible for
    creating a subtitle display element with version details.
    """

    @colorizer.Colorizer(style="version")
    def get_display(self) -> str:
        """
        Apply colorization to the subtitle text and return the display string
        with the software version tag.
        """

        version_details = software_version.SoftwareVersion()
        return f"Build: {version_details.version_tag}"


class DisplaySubtitle(Subtitle):
    """
    DisplaySubtitle class that inherits from Subtitle and is responsible for
    representing the subtitle as a string.
    """

    def __str__(self) -> str:
        """
        String representation of the DisplaySubtitle instance.
        """

        return self.get_display()
