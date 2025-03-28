from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

import build.tasks.components as task_components
import build.variables as variables


class TaskCreationError(Exception):
    """Custom exception for task creation errors."""


@dataclass
class AbstractTaskFactory(ABC):
    """Abstract base class for task factories."""

    @abstractmethod
    def create_task(self, task_name: str) -> Any:
        raise NotImplementedError()


@dataclass
class TaskFactory(AbstractTaskFactory):
    variable_manager: Optional[variables.VariableManager] = field(default=None)
    task_mapping: dict[str, type[Any]] = field(
        init=False,
        default_factory=lambda: dict(
            extract_payload_image=task_components.PayloadImageExtractor,
            rename_payload_image=task_components.PayloadImageRenamer,
            extract_stock_boot_image=task_components.BootImageExtractor,
            backup_stock_boot_image=task_components.StockBootImageBackupper,
            check_adb_connection=task_components.ADBConnectionChecker,
            push_stock_boot_image=task_components.StockBootImagePusher,
            find_patched_boot_image=task_components.MagiskImageFinder,
            pull_patched_boot_image=task_components.MagiskImagePuller,
            reboot_to_recovery=task_components.RecoveryRebooter,
            adb_sideload=task_components.ADBSideloader,
            reboot_to_bootloader=task_components.BootloaderRebooter,
            boot_magisk_image=task_components.MagiskImageBooter,
        ),
    )

    def create_task(self, task_name: str) -> Any:
        try:
            self.task_name = task_name
            task_class = self.task_mapping[task_name]
            return task_class(self.variable_manager)
        except KeyError:
            raise TaskCreationError(f"Task '{task_name}' is not recognized.")
