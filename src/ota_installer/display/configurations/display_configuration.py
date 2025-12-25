# src/ota_installer/display/configurations/display_configuration.py
from dataclasses import dataclass, field

from ...log_setup import logger
from ...program_versioning.constants.software_constants import (
    SoftwareConstants,
)
from ...program_versioning.containers.software_container import (
    SoftwareContainer,
)
from ...program_versioning.software_version import SoftwareVersion
from ..factories import DisplayFactory


@dataclass
class Configuration(object):  # Display Configuration
    software_version: "SoftwareVersion" = field(
        default_factory=SoftwareVersion
    )
    version_info: str = field(default_factory=str)

    def render_version_text(self) -> None:
        self.version_info = self.software_version.display

    def create_version_display(self) -> None:
        data = [enum_member.value for enum_member in SoftwareConstants]

        try:
            DisplayFactory.create_formatter(SoftwareContainer(*data))
        except AttributeError as err:
            logger.error(f"AttributeError: {err}")
        # except Exception as error:
        #    print(f"AFailed to create version display: {error}")

    def __str__(self) -> str:
        self.render_version_text()
        return ""


if __name__ == "__main__":
    pass
