# src/ota_installer/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorators
from ...variables import VariableManager
from ..constants.preparation_task_constants import PreparationTaskConstants
from ..operations.task_operation_details import TaskOperationDetails
from ..plugin_registry import task_plugin
from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.RENAME_PAYLOAD_IMAGE.value


@task_plugin(PreparationTaskConstants.RENAME_PAYLOAD_IMAGE.value)
@dataclass
class PayloadImageRenamer(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        source_path: Path = Path.home() / "payload.bin"
        command_string: str = (
            f"mv -v {source_path} {self.instance.file_paths['payload']}"
        )

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f"{ENUM_VALUES.TITLE.value} finished sucessfully!"
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
