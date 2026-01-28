# src/ota_installer/tasks/components/t12_magisk_image_booter.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.application_tasks import ApplicationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..operations.task_operation_processor import image_handler
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.BOOT_TO_MAGISK_IMAGE.value


@task_plugin(ApplicationTasks.BOOT_TO_MAGISK_IMAGE.value)
@dataclass
class MagiskImageBooter(BaseTask):
    """Task to flash a Magisk image to a device using fastboot."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for flashing the Magisk image."""
        device = self.instance.file_name.device
        partition: str = self._get_partition(device)
        command_string: str = self._build_command(partition)

        super().__init__(
            enum_values=ENUM_VALUES, command_string=command_string
        )

    def _get_partition(self, device: str) -> str:
        """Retrieves the partition name for the given device."""
        return image_handler(device).stem

    def _build_command(self, partition: str) -> str:
        """Constructs the fastboot command for flashing the Magisk image."""
        return f"fastboot flash {partition} {self.instance.file_paths.magisk}"

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.title} finished sucessfully!"
    )
    def perform_task(self) -> None:
        """Executes the task to flash the Magisk image."""
        self.task.run_with_output()


