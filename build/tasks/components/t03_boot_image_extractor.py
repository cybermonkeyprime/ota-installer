from dataclasses import dataclass, field
from pathlib import Path

from build.dispatchers import DispatcherManager, DispatcherTemplate
from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class BootImageExtractor(TaskFactoryTemplate):
    """
    Extracts boot images using a specified command string.

    Attributes:
        variable_manager: A instance of VariableManager to manage variables.
    """

    variable_manager: "type[VariableManager]" = field(default=VariableManager)

    index: int = 3
    title: str = "Boot Image Extractor"

    @property
    def command_string(self) -> str:
        """Generates the command string to extract the boot image."""
        device: str = self.variable_manager.file_name.parts.device
        source: Path = (
            Path.home()
            / self.variable_manager.boot_image.struct.payload.file_name
        )
        output_dir: Path = Path.home() / "images"
        options: str = (
            f"--images={self._retrieve_image_key(device)} --out {output_dir}"
        )
        return f"payload_dumper {source} {options}"

    def _retrieve_image_key(self, device: str) -> DispatcherTemplate:
        try:
            dispatcher = DispatcherManager("image")
            image_retriever = dispatcher.get_dispatcher()
            return image_retriever.get_key(device)
        except KeyError as err:
            raise ValueError(
                f"Invalid device for image retrieval: {device}"
            ) from err


def extract_boot_image(variable_manager: "type[VariableManager]"):
    extractor = BootImageExtractor(variable_manager=variable_manager)
    print(extractor.command_string)


if __name__ == "__main__":
    variable_manager_instance = VariableManager()
    extract_boot_image(variable_manager_instance)
