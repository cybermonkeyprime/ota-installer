from dataclasses import dataclass, field
from pathlib import Path

from dispatchers import DispatcherManager, DispatcherTemplate

from build.components.boot_image.structures.boot_image_file_structure import (
    BootImageFileStructure,
)
from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class StockBootImageBackupper(TaskFactoryTemplate):
    """
    A task for backing up the stock boot image.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        task_index: The index of the task in a sequence.
        task_title: The title of the task.
    """

    variable_manager: "type[VariableManager]" = field(default=VariableManager)
    index: int = field(default=4)
    title: str = field(default="Backup Stock Boot Image")

    @property
    def stock_image(self) -> BootImageFileStructure:
        return self.variable_manager.boot_image.struct.stock

    @property
    def device_name(self) -> str:
        return self.variable_manager.file_name.parts.device

    @property
    def source_path(self) -> Path:
        return (
            Path.home()
            / "images"
            / f"{self._retrieve_image_key(self.device_name)}.img"
        )

    @property
    def destination_path(self) -> Path:
        return Path.home().joinpath(
            self.stock_image.directory_path, self.stock_image.file_name
        )

    @property
    def command_string(self) -> str:
        return f"cp -v {self.source_path} {self.destination_path}"

    def _retrieve_image_key(self, device: str) -> DispatcherTemplate:
        try:
            dispatcher = DispatcherManager("image")
            image_retriever = dispatcher.get_dispatcher()
            return image_retriever.get_key(device)
        except KeyError as err:
            raise ValueError(
                f"Invalid device for image retrieval: {device}"
            ) from err

    def execute_backup(self) -> None:
        try:
            result = Path(self.command_string).read_text()
            print(f"Backup successful: {result}")
        except Exception as e:
            print(f"Backup failed: {e}")


def main():
    backup_task = StockBootImageBackupper()
    backup_task.execute_backup()


if __name__ == "__main__":
    main()
