from dataclasses import field

import src.display.formatters as display_formatters


class DisplayFactory(object):
    @staticmethod
    def create_formatter(
        title: str = field(default="Title"),
        major_number: int = field(default=1),
        minor_number: int = field(default=1),
        patch_number: int = field(default=1),
    ) -> display_formatters.DisplayFormatter:
        return display_formatters.DisplayFormatter(
            title=title,
            major_number=major_number,
            minor_number=minor_number,
            patch_number=patch_number,
        )


if __name__ == "__main__":
    formatter = DisplayFactory.create_formatter()
