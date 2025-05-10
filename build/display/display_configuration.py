from dataclasses import dataclass, field

import build.display as display
from build.program_versioning import VersionDetails


@dataclass
class DisplayConfiguration(object):
    software_version: VersionDetails = field(default_factory=VersionDetails)
    version_info: str = field(default_factory=str)

    def render_version_text(self) -> None:
        self.version_info = str(self.software_version.version_tag)

    def create_version_display(self) -> None:
        try:
            display.DisplayFactory.create_formatter(
                title=self.software_version.title,
                major_number=self.software_version.major_number,
                minor_number=self.software_version.minor_number,
                patch_number=self.software_version.patch_number,
            )
        except Exception as error:
            print(f"Failed to create version display: {error}")

    def __str__(self) -> str:
        self.render_version_text()
        return f"SoftwareVersion: {self.software_version.title}-{self.version_info}"


if __name__ == "__main__":
    software_version = VersionDetails(
        title="ExampleTitle", major_number=1, minor_number=2, patch_number=0
    )
    display_config = DisplayConfiguration(software_version=software_version)
    print(display_config)
