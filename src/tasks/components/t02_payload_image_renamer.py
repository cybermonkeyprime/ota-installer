# src/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

import src.variables as variables
from src import decorators
from src.tasks.task_operation_details import TaskOperationDetails

from .base_task import BaseTask

ENUM_VALUES = TaskOperationDetails.PAYLOAD_IMAGE_RENAMER.value

print(f"{ENUM_VALUES=}")


@dataclass
class PayloadImageRenamer(BaseTask):
    instance: variables.VariableManager = field(
        default_factory=variables.VariableManager
    )

    def __post_init__(self) -> None:
        source_path: Path = Path.home() / "payload.bin"
        destination_path = self.instance.boot_image_paths.payload
        command_string: str = f"mv -v {source_path} {destination_path}"

        super().__init__(
            enum_values=ENUM_VALUES,
            command_string=command_string,
        )

    @decorators.DoublePaddedFooterWrapper(
        message=f'Task: "{ENUM_VALUES.TITLE.value}" Completed'
    )
    def perform_task(self) -> None:
        self.task.run_with_output()
