from dataclasses import field

from ..formatters.display_formatter import DisplayFormatter


class DisplayFactory:
    @staticmethod
    def create_formatter(
        title: str = field(default="Title"),
        major_number: int = field(default=0),
        minor_number: int = field(default=0),
        patch_number: int = field(default=0),
    ) -> DisplayFormatter:
        return DisplayFormatter(
            title=title,
            major_number=major_number,
            minor_number=minor_number,
            patch_number=patch_number,
        )


if __name__ == "__main__":
    # formatter = DisplayFactory.create_formatter()
    pass
