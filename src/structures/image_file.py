from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ImageFile(object):
    file_name: Path = field(default_factory=Path)
    directory_path: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        self.file_path = self.file_name

    def get_full_path(self) -> Path:
        return Path(self.directory_path) / self.file_name

    def __str__(self) -> str:
        return str(self.get_full_path())
