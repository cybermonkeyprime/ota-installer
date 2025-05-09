from dataclasses import dataclass


from build.program_versioning import VersionDetails


@dataclass
class VersionManager(object):
    """
    Manages the creation of VersionDetails instances.
    """

    def create_detailed_version(
        self, major_number: int, minor_number: int, patch_number: int
    ) -> VersionDetails:
        """
        Creates a VersionDetails instance with the given build and revision numbers.

        Args:
            build: The build number of the version.
            revision: The revision number of the version.

        Returns:
            A VersionDetails instance with the specified build and revision.
        """
        return VersionDetails(
            major_number=major_number,
            minor_number=minor_number,
            patch_number=patch_number,
        )


def display_version_info(version: VersionDetails) -> None:
    """
    Displays the version information of a VersionDetails instance.

    Args:
        version: The VersionDetails instance whose information is to be displayed.
    """
    print(version.version_info)


def main(version_manager: VersionManager) -> None:
    """
    The main function that creates and displays version information.

    Args:
        version_manager: An instance of VersionManager to create VersionDetails.
    """
    detailed_version = version_manager.create_detailed_version(1, 2, 3)
    display_version_info(detailed_version)


if __name__ == "__main__":
    try:
        version_manager = VersionManager()
        main(version_manager)
    except Exception as error:
        print(f"An error occurred: {error}")
