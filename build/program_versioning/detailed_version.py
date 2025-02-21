from dataclasses import dataclass

from build.program_versioning.base_version import BaseVersion


@dataclass
class DetailedVersion(BaseVersion):
    @property
    def version_info(self) -> str:
        return (
            f"{self.title} Build: {self.build_number}, Revision: {self.revision_number}"
        )


if __name__ == "__main__":
    pass
