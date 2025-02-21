from dataclasses import dataclass

from build.software_versioning.detailed_verion import DetailedVersion


@dataclass
class VersionManager(object):
    def create_detailed_version(self, build: int, revision: int) -> DetailedVersion:
        return DetailedVersion(build_number=build, revision_number=revision)


def display_version_info(version: DetailedVersion) -> None:
    print(version.version_info)


def main() -> None:
    version_manager = VersionManager()
    detailed_version = version_manager.create_detailed_version(1, 2)
    display_version_info(detailed_version)


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"An error occurred: {error}")
