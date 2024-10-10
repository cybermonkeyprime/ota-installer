from dataclasses import dataclass, field

from .base_version import BaseVersion


@dataclass
class DetailedVersion(BaseVersion):
    version_info: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.version_info = (
            f"{self.title} Build: {self.build_number}, Revision: {self.revision_number}"
        )


if __name__ == "__main__":
    pass
