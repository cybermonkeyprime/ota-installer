from dataclasses import dataclass


@dataclass
class BaseVersion(object):
    title: str = "OTA-Installer"
    build_number: int = 20250328  # YYYYMMDD
    revision_number: int = 280130  # ddhhmm

    @property
    def tag(self) -> str:
        return f"v{self.build_number}.{self.revision_number}"
