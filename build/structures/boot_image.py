from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BootImage:
    parent_directory: str
    stock: Path = field(default_factory=Path)
    magisk: Path = field(default_factory=Path)

    def __post_init__(self) -> None:
        self.stock = Path.home().joinpath(self.parent_directory, "stock")
        self.magisk = Path.home().joinpath(self.parent_directory, "magisk")

    def __str__(self) -> str:
        return self.parent_directory
