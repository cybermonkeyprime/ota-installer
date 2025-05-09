from dataclasses import dataclass

from build.decorators import Colorizer
from build.display.display_template import DisplayComponent
from build.program_versioning.version_details import VersionDetails


@dataclass
class Subtitle(DisplayComponent):
    @Colorizer(style="version")
    def get_display(self) -> str:
        version_details = VersionDetails()
        return f"Build: {version_details.version_info}"


class DisplaySubtitle(Subtitle):
    def __str__(self) -> str:
        return self.get_display()
