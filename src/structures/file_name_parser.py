from dataclasses import dataclass, field
from pathlib import Path
from typing import Self


@dataclass
class FileNameParser:
    raw_name: Path
    parts: list[str] = field(init=False)
    device: str = field(init=False)
    file_type: str = field(init=False)
    version: str = field(init=False)
    extra: str | None = field(init=False)

    def __post_init__(self) -> None:
        self.parse_file_name()

    def set_raw_name(self, path: Path) -> Self:
        self.raw_name = Path(path)
        return self

    def parse_file_name(self) -> None:
        self.parts = str(self.raw_name).split("-")
        try:
            self.device, self.file_type, self.version, *extra_parts = (
                self.parts
            )
            self.extra = "-".join(extra_parts) if extra_parts else None
        except ValueError as err:
            raise ValueError(
                f"Error parsing file name: {self.raw_name}"
            ) from err

    def __str__(self) -> str:
        return str(self.raw_name)


if __name__ == "__main__":
    file_name = Path("device-type-version-extra-info")
    FileNameParser(file_name)  # .set_raw_name(file_name).parse_file_name()
