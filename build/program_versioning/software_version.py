from dataclasses import dataclass, field


@dataclass
class SoftwareVersion(object):
    """
    Represents a base version with a title, build number, and revision number.

    Attributes:
        title (str): The title of the software.
        build_number (int): The build number in YYYYMMDD format.
        revision_number (int): The revision number in ddhhmm format.
    """

    title: str = "OTA-Installer"
    major_number: int = field(default=2025)
    minor_number: int = field(default=5)
    patch_number: int = field(default=1)

    @property
    def version_tag(self) -> str:  # possibly rename to version_tag
        """Generates a version tag string."""
        return f"{self.major_number}.{self.minor_number}.{self.patch_number}"


if __name__ == "__main__":
    # Example usage
    software_version = SoftwareVersion()
    print(software_version.version_tag)
