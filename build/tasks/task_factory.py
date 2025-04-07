from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Dict

from build.tasks import components as task_components
from build.variables import VariableManager

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
    """Factory class to create task objects based on a given task name.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        task_mapping: A dictionary mapping task names to their respective classes.
    """
    variable_manager: Optional[VariableManager] = field(default=None)
    task_mapping: Dict[str, type] = field(
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
    ) # add task_components.TaskComponent as return type

    def create_task(self, task_name: str) -> Any: # add task_components.TaskComponent as return type
        """Creates a task object based on the task name.

        Args:
            task_name: The name of the task to create.

        Returns:
            An instance of the task class associated with the task name.

        Raises:
            TaskCreationError: If the task name is not recognized.
        """
        try:
            self.task_name = task_name
            task_class = self.task_mapping[task_name]
            return task_class(self.variable_manager)
        except KeyError:
            raise TaskCreationError(f"Task '{task_name}' is not recognized.")
