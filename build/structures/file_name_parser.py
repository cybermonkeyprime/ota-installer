from dataclasses import dataclass, field
from typing import List


@dataclass
class FileNameParser:
    raw_name: str
    parts: List[str] = field(init=False)
    device: str = field(init=False)
    file_type: str = field(init=False)
    version: str = field(init=False)
    extra: str | None = field(init=False)

    def __post_init__(self) -> None:
        self.parse_file_name()

    def parse_file_name(self) -> None:
        self.parts = self.raw_name.split("-")
        try:
            self.device, self.file_type, self.version, *extra_parts = self.parts
            self.extra = "-".join(extra_parts) if extra_parts else None
        except ValueError as e:
            raise ValueError(f"Error parsing file name: {self.raw_name}") from e

    def __str__(self) -> str:
        return self.raw_name


if __name__ == "__main__":
    file_name = "device-type-version-extra-info"
    FileNameParser(raw_name=file_name)
