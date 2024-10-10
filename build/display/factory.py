from dataclasses import field

import build.display.formatter as _formatter


class Factory:
    @staticmethod
    def create_formatter(
        title: str = field(default="Title"),
        build: int = field(default=1),
        revision: int = field(default=1),
    ) -> _formatter.Formatter:
        return _formatter.Formatter(
            title=title,
            build=build,
            revision=revision,
        )


if __name__ == "__main__":
    formatter = Factory.create_formatter()
