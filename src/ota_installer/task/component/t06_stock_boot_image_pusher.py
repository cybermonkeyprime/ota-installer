# src/ota_installer/tasks/components/t06_stock_boot_image_pusher.py
from dataclasses import dataclass, field
from pathlib import Path

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task_group.task_group_pipeline import MIGRATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = MIGRATION[1]
TITLE = STEP.name


@dataclass
class StockBootImagePusher(BaseTask):
    """Task to push the stock boot image to the device using adb."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the command string for pushing the stock boot image."""
        command_string = self._create_adb_push_command()

        super().__init__(
            enum_values=STEP,
            command_string=command_string,
            reminder=STEP.reminder,
        )

    def _create_adb_push_command(self) -> str:
        """Creates the adb push command string."""
        stock_image_path = Path(self.instance.file_paths.stock)
        return f'adb push "{stock_image_path}" /sdcard/'

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the task to push the stock boot image."""
        self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class StockBootImagePusherPlugin(StockBootImagePusher):
    """Plugin for the StockBootImagePusher task."""

    pass


# Signed off by Brian Sanford on 20260625
