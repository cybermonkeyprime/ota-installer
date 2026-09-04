# src/ota_installer/tasks/components/t02_payload_image_renamer.py
from dataclasses import dataclass, field
from pathlib import Path

from ...plugin.plugin_registry import Plugin
from ...style import decorator
from ...task.task_group.task_group_pipeline import PREPARATION
from ...variable.variable_director import VariableDirector
from .base_task import BaseTask

STEP = PREPARATION[1]
TITLE = STEP.name


@dataclass
class PayloadImageRenamer(BaseTask):
    """Renames the payload image file to a specified path."""

    instance: VariableDirector = field(default_factory=VariableDirector)

    def __post_init__(self) -> None:
        """Initializes the command string for renaming the payload image."""

        super().__init__(
            enum_values=STEP,
            command_string=self._create_rename_command(),
        )

    def _create_rename_command(self) -> str:
        """Generates the command string for renaming the payload image."""
        source_path = Path.home() / "payload.bin"
        destination_path = self.instance.file_paths.payload
        return f"mv -v {source_path} {destination_path}"

    @decorator.DoublePaddedFooterWrapper(message=f"{STEP.success_message}")
    def perform_task(self) -> None:
        """Executes the task to rename the payload image."""
        if self.task:
            self.task.run_with_output()


@Plugin.TASK.register(TITLE.lower())
@dataclass
class PayloadImageRenamerPlugin(PayloadImageRenamer):
    """Plugin for the PayloadImageRenamer task."""

    pass


# Signed off by Brian Sanford on 20260626
