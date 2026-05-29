# src/ota_installer/tasks/components/t07_magisk_image_finder.py
from dataclasses import dataclass, field
from pathlib import Path

from ... import decorator
from ...plugin.plugin_registry import task_plugin
from ...task.task_group_handler import MigrationTask
from ...task.task_info import TaskID
from ...variable.variable_manager import VariableManager
from .base_task import BaseTask

TITLE = TaskID.FIND_MAGISK_IMAGE


@dataclass
class MagiskImageFinder(BaseTask):
    instance: VariableManager = field(default_factory=VariableManager)

    def __post_init__(self) -> None:
        remote_path = Path(self.instance.directories.magisk.remote_path)
        command_string = self._create_command_string(remote_path)
        super().__init__(
            enum_values=TITLE.enum_values,
            command_string=command_string,
        )

    def _create_command_string(self, remote_path: Path) -> str:
        """Constructs the command string to locate the patched boot image."""
        return f"adb shell ls {remote_path} | grep magisk_patched | head -n1"

    @decorator.DoublePaddedFooterWrapper(message=f"{TITLE.success_message}")
    def perform_task(self) -> None:
        """Executes the task of locating the patched boot image."""
        self.task.show_index_and_title()
        if getattr(self.task, "description", None):
            self.task.show_description()

        result = self.task.execute_and_return_output("Patched Boot Image")
        if result:
            self.instance.image_name["patched"] = result
            print(f"{self.instance.image_name["patched"]=}")
        if getattr(self.task, "reminder", None):
            self.task.show_reminder()


@task_plugin(MigrationTask[TITLE.name].value)
@dataclass
class MagiskImageFinderPlugin(MagiskImageFinder):
    """Plugin for the MagiskImageFinder task."""

    pass


# Signed off by Brian Sanford on 20260528
