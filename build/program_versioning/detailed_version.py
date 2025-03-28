from dataclasses import dataclass

from build.program_versioning.base_version import BaseVersion


@dataclass
class DetailedVersion(BaseVersion):
    @property
    def version_info(self) -> str:
        return f"{self.title} Build: {self.tag}"


if __name__ == "__main__":
    pass
