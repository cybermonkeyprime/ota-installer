# src/ota_installer/tasks/managers/task_director.py

from collections.abc import Callable

from ...log_setup import logger
from ...variables.variable_manager import VariableManager


def task_director(instance: VariableManager, task_name: Callable) -> None:
    """Manages the initiation of task processing."""
    logger.debug(f"Initiating task: {task_name}")
    task = task_name(instance=instance)

    if not _is_executable(task):
        logger.error(f"Task {task_name!r} is missing perform_task() method.")
        raise ValueError(f"Task {task_name!r} is not executable.")

    task.perform_task()


def _is_executable(task: object) -> bool:
    """Checks if the task has a perform_task method."""
    return hasattr(task, "perform_task")
