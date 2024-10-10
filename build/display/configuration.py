from dataclasses import dataclass, field

import build.display as display
import build.software_versioning as versioning


@dataclass
class Configuration(object):  # Display Configuration
    software_version: versioning.DetailedVersion = field(
        default_factory=versioning.DetailedVersion
    )
    version_info: str = field(default_factory=str)

    def render_version_text(self) -> None:
        self.version_info = str(self.software_version.build_number)
        if self.software_version.revision_number != 0:
            self.version_info += f"-{self.software_version.revision_number}"

    def create_version_display(self) -> None:
        try:
            display.Factory.create_formatter(
                title=self.software_version.title,
                build=self.software_version.build_number,
                revision=self.software_version.revision_number,
            )
        except Exception as error:
            print(f"Failed to create version display: {error}")

    def __str__(self) -> str:
        self.render_version_text()
        return f"SoftwareVersion: {self.software_version.title}-{self.version_info}"


if __name__ == "__main__":
    software_version = versioning.DetailedVersion(
        title="ExampleTitle", build_number=1, revision_number=2
    )
    display_config = Configuration(software_version=software_version)
    print(display_config)
