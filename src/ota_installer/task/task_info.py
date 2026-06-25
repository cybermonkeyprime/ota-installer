# tasks/task_info.py
from collections.abc import Callable
from enum import StrEnum, auto

from ..plugin.plugin_registry import TASK_PLUGINS
from ..style.style_info import indentation
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


