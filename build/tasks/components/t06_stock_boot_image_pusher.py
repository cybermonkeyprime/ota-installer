from dataclasses import dataclass, field
from pathlib import Path

from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class StockBootImagePusher(TaskFactoryTemplate):
    """
    A class responsible for pushing the stock boot image to a device.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        index: The index of the task in a sequence of tasks.
        title: The title of the task.
        comment_string: An aftertask instruction.
    """

    variable_manager: "type[VariableManager]" = field(default=VariableManager)
    index: int = 2
    title: str = "Push Stock Boot Image"
    comment_string: str = field(default="Patch boot image in Magisk app")

    @property
    def stock_boot_image_path(self) -> Path:
        """
        Returns the path to the stock boot image.

        Returns:
            The Path object representing the path to the stock boot image.
        """
        boot_image = self.variable_manager.boot_image.struct.stock
        return Path.home() / boot_image.directory_path / boot_image.file_name

    @property
    def command_string(self) -> str:
        """
        Constructs the ADB command to push the boot image to the device.

        Returns:
            The ADB command as a string.
        """
        return f"adb push {self.stock_boot_image_path} /sdcard/"
