# src/ota_installer/tasks/managers/task_director.py

from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from ..factories.task_factory import TaskFactory


def task_director(instance: VariableManager, task_name: str) -> None:
    """Manages the initiation of task processing."""
    logger.debug(f"task_director(): {task_name=}")
    task = TaskFactory(instance).create_task(task_name=task_name)
    logger.debug(f"task_director(): {task=}")
    if task is None:
        logger.error(
            f"Failed to resolve task: {task_name!r} — task returned None"
        )
        return  # or raise an exception if desired
    try:
        task.perform_task()
    except AttributeError as err:
        logger.error(f"Task {task_name!r} is missing perform_task(): {err}")
    except Exception as err:
        logger.exception(
            f"Unexpected error while executing {task_name!r}: {err}"
        )


# Signed off by Brian Sanford on 20260203
