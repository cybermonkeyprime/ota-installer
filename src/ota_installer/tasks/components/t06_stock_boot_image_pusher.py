# src/ota_installer/tasks/components/t06_stock_boot_image_pusher.py
from dataclasses import dataclass, field

from ... import decorators
from ...task_groups.constants.migration_tasks import MigrationTasks
from ...variables.variable_manager import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PUSH_STOCK_BOOT_IMAGE.value


@task_plugin(MigrationTasks.PUSH_STOCK_BOOT_IMAGE.value)
@dataclass
class StockBootImagePusher(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        command_string = (
            f'adb push "{self.instance.file_paths["stock"]}" /sdcard/'
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
            reminder=ENUM_VALUES.REMINDER.value,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
