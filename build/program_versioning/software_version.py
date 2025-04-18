from dataclasses import dataclass, field


@dataclass
class SoftwareVersion(object): # Possibly rename to SoftwareVersion
    """
    Represents a base version with a title, build number, and revision number.

    Attributes:
        title (str): The title of the software.
        build_number (int): The build number in YYYYMMDD format.
        revision_number (int): The revision number in ddhhmm format.
    """
    title: str = "OTA-Installer"
    build_number: int = field(default=20250408) # YYYYMMDD, Y = year, M = month, D = date
    revision_number: int = field(default=80430) # DDhhmm, D = date, h = hour, m = minute

    @property
    def version_tag(self) -> str: # possibly rename to version_tag
        """Generates a version tag string."""
        return f"v{self.build_number}.{self.revision_number}"

if __name__ == '__main__':
    # Example usage
    software_version = SoftwareVersion()
    print(software_version.version_tag)

