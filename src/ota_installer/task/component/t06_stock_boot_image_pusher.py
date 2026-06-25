# src/ota_installer/tasks/components/t06_stock_boot_image_pusher.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_info import MigrationTask
from ...task.task_info import TaskID
from ...variable.variable_manager import VariableManager
from .base_task import BaseTask

TITLE = TaskID.PUSH_STOCK_IMAGE


@dataclass
class StockBootImagePusher(BaseTask):
    """Task to push the stock boot image to the device using adb."""

    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        """Initializes the command string for pushing the stock boot image."""
        command_string = self._create_adb_push_command()

        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=command_string,
            reminder=TITLE.enum_values.reminder,
        )

    def _create_adb_push_command(self) -> str:
        """Creates the adb push command string."""
        stock_image_path = Path(self.instance.file_paths.stock)
        return f'adb push "{stock_image_path}" /sdcard/'

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task to push the stock boot image."""
        self.task.run_with_output()


@task_plugin(MigrationTask[TITLE.name].value)
@dataclass
class StockBootImagePusherPlugin(StockBootImagePusher):
    """Plugin for the StockBootImagePusher task."""

    pass


