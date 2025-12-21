# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...task_groups.constants.preparation_tasks import PreparationTasks
from ...variables import VariableManager
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.EXTRACT_PAYLOAD_IMAGE.value


@task_plugin(PreparationTasks.EXTRACT_PAYLOAD_IMAGE.task_name)
@dataclass
class PayloadImageExtractor(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self):
        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=(
                f'unzip -o "{self.instance.path}" payload.bin -d "{Path.home()}"'
            ),
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
