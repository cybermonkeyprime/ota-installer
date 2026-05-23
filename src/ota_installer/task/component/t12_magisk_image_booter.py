# src/ota_installer/tasks/components/t12_magisk_image_booter.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_handler import ApplicationTask
from ...variable.variable_manager import VariableManager
from ..operation.task_operation_details import TaskOperationDetails
from ..operation.task_operation_processor import image_handler
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BOOT_TO_MAGISK_IMAGE.value


@task_plugin(name=ApplicationTask.BOOT_TO_MAGISK_IMAGE.value)
@dataclass
class MagiskImageBooter(BaseTask):
    """Task to flash a Magisk image to a device using fastboot."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for flashing the Magisk image."""
        device: str = self.instance.file_name.device
        partition: str = self._get_partition(device)
        command_string: str = self._build_command(partition)

        super().__init__(
            enum_values=ENUM_VALUES, command_string=command_string
        )

    def _get_partition(self, device: str) -> str:
        """Retrieves the partition name for the given device."""
        partition_path: Path = image_handler(device)
        return partition_path.stem

    def _build_command(self, partition: str) -> str:
        """Constructs the fastboot command for flashing the Magisk image."""
        magisk_path = Path(self.instance.file_paths.magisk)
        return f"fastboot flash {partition} {magisk_path}"

    @decorator.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to flash the Magisk image."""
        self.task.run_with_output()
