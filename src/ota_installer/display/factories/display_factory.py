# src/ota_installer/display/factories/display_factory.py
from ...program_versioning.software_version import (
    SoftwareContainer,
    SoftwareVersionConstants,
)
from ..formatters import DisplayFormatter


class DisplayFactory(object):
    @staticmethod
    def create_formatter(
        data=SoftwareContainer(
            *[enum_member.value for enum_member in SoftwareVersionConstants]
        ),
    ) -> DisplayFormatter:
        return DisplayFormatter(*data)


if __name__ == "__main__":
    formatter = DisplayFactory.create_formatter()
