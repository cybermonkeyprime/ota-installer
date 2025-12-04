from dataclasses import dataclass, field

from src.software_version import SoftwareVersion

from .display_factory import DisplayFactory


@dataclass
class DisplayConfiguration(SoftwareVersion):
    version_info: str = field(default_factory=str)

    def render_version_text(self) -> None:
        self.version_info = str(self.build_number)
        if self.revision_number != 0:
            self.version_info += f"-{self.revision_number}"

    def create_version_display(self) -> None:
        try:
            DisplayFactory.create_formatter(
                title=self.title,
                build=self.build_number,
                revision=self.revision_number,
            )
        except Exception as error:
            print(f"BFailed to create version display: {error}")

    def __str__(self) -> str:
        self.render_version_text()
        return f"SoftwareVersion: {self.title}-{self.version_info}"
