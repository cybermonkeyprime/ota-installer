# src/ota_installer/display/factories/display_factory.py
from ...program_versioning.builders.software_container_builder import (
    build_software_container,
)
from ..formatters import DisplayFormatter


class DisplayFactory(object):
    @staticmethod
    def create_formatter() -> DisplayFormatter:
        return create_formatter()


def create_formatter() -> DisplayFormatter:
    sc = build_software_container()
    return DisplayFormatter(
        title=sc.title,
        major_number=sc.major_number,
        minor_number=sc.minor_number,
        patch_number=sc.patch_number,
    )


if __name__ == "__main__":
    formatter = create_formatter()
