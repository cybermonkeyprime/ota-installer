# tasks/task_info.py
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from enum import StrEnum, auto

from ..plugin.plugin_registry import TASK_PLUGINS
from ..style.style_handler import indentation
from .operation.task_operation_info import (
    TaskOperationContainer,
    get_task_detail,
)


class TaskID(StrEnum):
    """Enumeration of task identifiers for OTA installation processes."""

    # preparation
    EXTRACT_PAYLOAD_IMAGE = auto()
    RENAME_PAYLOAD_IMAGE = auto()
    EXTRACT_STOCK_BOOT_IMAGE = auto()
    BACKUP_STOCK_BOOT_IMAGE = auto()
    # migration
    CHECK_ADB_CONNECTION = auto()
    PUSH_STOCK_IMAGE = auto()
    FIND_MAGISK_IMAGE = auto()
    PULL_MAGISK_IMAGE = auto()
    # application
    REBOOT_TO_RECOVERY = auto()
    APPLY_OTA_UPDATE = auto()
    REBOOT_TO_BOOTLOADER = auto()
    BOOT_TO_MAGISK_IMAGE = auto()

    @property
    def execute(self) -> Callable | None:
        """
        The Dispatcher: Fetches the registered plugin function.
        Fails loudly if the task exists in TaskID but wasn't loaded.
        """
        if self.value not in TASK_PLUGINS:
            raise NotImplementedError(
                f"LOUD FAIL: TaskID.{self.name} ('{self.value}') has no "
                f"registered plugin. Check plugin_loader.py imports!"
            )

        return TASK_PLUGINS.get(self.value)

    @property
    def enum_values(self) -> TaskOperationContainer:
        return get_task_detail(self.name)

    @property
    def success_message(self) -> str:
        return (
            f"{indentation(2)}"
            f"{self.value.lower().replace('_', ' ').capitalize()} finished successfully!"
        )


@dataclass(frozen=True, slots=True)
class TaskRenderer:
    """Container for task information."""

    task_class: type
    task_name: str

    def __call__(self, *args, **kwargs) -> tuple:
        """
        Executes the task's generation logic wrapped in the required UI
            decorators.
        """
        from .. import decorator

        # 1. This encapsulates your internal execution context
        def result():
            return self.task_class.get_member_names()

        # 2. Define the execution closure and apply your outer decorator
        @decorator.PaddedFooterWrapper()
        def execute_pipeline():
            # Apply your dynamic inner decorator
            decorated_function: Callable = decorator.ConfirmationPrompt(
                char=" ", comment=f"perform the {self.task_name}s"
            )(result)

            return decorated_function()

        # 3. Fire the pipeline and hand back the final tuple payload
        return execute_pipeline()


def fetch_task_mapping() -> Mapping[str, TaskRenderer]:
    from ..task.task_group_handler import (
        ApplicationTask,
        MigrationTask,
        PreparationTask,
        TaskGroupName,
    )

    return {
        TaskGroupName.PREPARATION.value: TaskRenderer(
            PreparationTask, "Preparation Task"
        ),
        TaskGroupName.MIGRATION.value: TaskRenderer(
            MigrationTask, "Migration Task"
        ),
        TaskGroupName.APPLICATION.value: TaskRenderer(
            ApplicationTask, "Application Task"
        ),
    }


TASK_GROUP_MAPPING = fetch_task_mapping()
# Signed off by Brian Sanford on 20260528
