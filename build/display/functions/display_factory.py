from dataclasses import field
from .display_formatter import DisplayFormatter


class DisplayFactory:
    @staticmethod
    def create_formatter(
        title: str = field(default="Title"),
        build: int = field(default=1),
        revision: int = field(default=1),
    ) -> DisplayFormatter:
        return DisplayFormatter(
            title=title,
            build=build,
            revision=revision,
        )


if __name__ == "__main__":
    # formatter = DisplayFactory.create_formatter()
    pass
