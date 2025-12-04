from dataclasses import dataclass, field

import src.display.factories as display_factories
import src.program_versioning.software_version as software_version


@dataclass
class Configuration(object):  # Display Configuration
    software_version: "software_version.SoftwareVersion" = field(
        default_factory=software_version.SoftwareVersion
    )
    version_info: str = field(default_factory=str)

    def render_version_text(self) -> None:
        self.version_info = self.software_version.version_tag

    def create_version_display(self) -> None:
        try:
            display_factories.DisplayFactory.create_formatter(
                title=self.software_version.constants.TITLE,
                major_number=self.software_version.constants.MAJOR_NUMBER,
                minor_number=self.software_version.constants.MINOR_NUMBER,
                patch_number=self.software_version.constants.PATCH_NUMBER,
            )
        except AttributeError as err:
            print(f"AttributeError: {err}")
        # except Exception as error:
        #    print(f"AFailed to create version display: {error}")

    def __str__(self) -> str:
        self.render_version_text()
        return ""

        # return f"""
        # SoftwareVersion: {self.software_version.title}-{self.version_info}
        # """


if __name__ == "__main__":
    pass
