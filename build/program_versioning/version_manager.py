from dataclasses import dataclass


from build.program_versioning import DetailedVersion


@dataclass
class VersionManager(object):
    """
    Manages the creation of DetailedVersion instances.
    """


    def create_detailed_version(self, build: int, revision: int) -> DetailedVersion:
        """
        Creates a DetailedVersion instance with the given build and revision numbers.

        Args:
            build: The build number of the version.
            revision: The revision number of the version.

        Returns:
            A DetailedVersion instance with the specified build and revision.
        """
        return DetailedVersion(build_number=build, revision_number=revision)


def display_version_info(version: DetailedVersion) -> None:
    """
    Displays the version information of a DetailedVersion instance.

    Args:
        version: The DetailedVersion instance whose information is to be displayed.
    """
    print(version.version_info)


def main(version_manager: VersionManager) -> None:
    """
    The main function that creates and displays version information.

    Args:
        version_manager: An instance of VersionManager to create DetailedVersion.
    """
    detailed_version = version_manager.create_detailed_version(1, 2)
    display_version_info(detailed_version)


if __name__ == "__main__":
    try:
        version_manager = VersionManager()
        main(version_manager)
    except Exception as error:
        print(f"An error occurred: {error}")
