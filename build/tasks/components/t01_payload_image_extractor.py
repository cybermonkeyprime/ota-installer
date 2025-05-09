from dataclasses import dataclass, field
from pathlib import Path

from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class PayloadImageExtractor(TaskFactoryTemplate):
    """
    Extracts a payload image from a given file path and stores it in the user's
    home directory.
    """

    instance: VariableManager = field(default_factory=VariableManager)

    index: int = 1
    title: str = "Payload Image Extractor"

    @property
    def command_string(self) -> str:
        """Generates the command string to extract the payload image."""
        try:
            file_path = self.instance.file_path
            return f"unzip -o {file_path} payload.bin -d {Path.home()}"
        except AttributeError as err:
            raise ValueError(
                "VariableManager must have a 'file_path' attribute"
            ) from err
