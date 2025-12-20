# src/ota_installer/tasks/components/t01_payload_image_extractor.py
from pathlib import Path

from ... import decorators
from ..constants.preparation_task_constants import PreparationTaskConstants
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.EXTRACT_PAYLOAD_IMAGE.value


@task_plugin(PreparationTaskConstants.EXTRACT_PAYLOAD_IMAGE.value)
class PayloadImageExtractor(BaseTask):
    def __init__(self, instance):
        self.instance = instance
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
