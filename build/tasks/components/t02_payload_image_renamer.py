from dataclasses import dataclass, field
from pathlib import Path

from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class PayloadImageRenamer(TaskFactoryTemplate):
    """
    A class responsible for renaming payload images according to the
    provided variable manager's boot image structure.

    Attributes:
        instance (VariableManager): The manager that holds variables
            for the boot image structure.
        index (int): The index used in renaming, if applicable.
        title (str): The title of the task.
    """

    instance: VariableManager = field(default_factory=VariableManager)
    index: int = 2
    title: str = "Payload Image Renamer"

    @property
    def command_string(self) -> str:
        """Generates the command string to rename the payload image."""
        source_path = Path.home() / "payload.bin"
        destination_path = (
            Path.home()
            / self.instance.boot_image.image_structure.payload.file_name
        )

        return f"mv -v {source_path} {destination_path}"
