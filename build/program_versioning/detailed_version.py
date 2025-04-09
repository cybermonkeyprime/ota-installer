from dataclasses import dataclass

from build.program_versioning import BaseVersion


@dataclass
class DetailedVersion(BaseVersion): # Possibly rename to VersionDetails
    """
    Represents detailed information about a version, including title and tag.

    """

    @property
    def version_info(self) -> str:
        """Constructs a detailed version string."""
        return f"{self.title} Build: {self.tag}"

def display_version_info(version_details: DetailedVersion):
    """
    Prints the version information.

    Args:
        version_details (VersionDetails): The version details to display.
    """
    try:
        print(version_details.version_info)
    except AttributeError as error:
        print(f"Error displaying version info: {error}")


if __name__ == "__main__":
    version = DetailedVersion(title="My Application")
    display_version_info(version)
