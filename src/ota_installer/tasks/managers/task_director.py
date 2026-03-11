# src/ota_installer/tasks/managers/task_director.py

from collections.abc import Callable

from ...log_setup import logger
from ...variables.variable_manager import VariableManager


def task_director(instance: VariableManager, task_name: Callable) -> None:
    """Manages the initiation of task processing."""
    logger.debug(f"Initiating task: {task_name}")
    task = task_name(instance=instance)

    if not hasattr(task, "perform_task"):
        logger.error(f"Task {task_name!r} is missing perform_task() method.")
        raise ValueError(f"Task {task_name!r} is not executable.")

    task.perform_task()


# Signed off by Brian Sanford on 20260305
