# src/ota_installer/display/factories/display_factory.py
from dataclasses import field

from ..formatters import DisplayFormatter


class DisplayFactory(object):
    @staticmethod
    def create_formatter(
        title: str = field(default="Title"),
        major_number: int = field(default=1),
        minor_number: int = field(default=1),
        patch_number: int = field(default=1),
    ) -> DisplayFormatter:
        return DisplayFormatter(
            title=title,
            major_number=major_number,
            minor_number=minor_number,
            patch_number=patch_number,
        )


if __name__ == "__main__":
    formatter = DisplayFactory.create_formatter()
