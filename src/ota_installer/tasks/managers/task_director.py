# src/ota_installer/tasks/managers/task_director.py

from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from ..factories import TaskFactory


def task_director(instance: VariableManager, item: str) -> None:
    """Manages the initiation of task processing."""
    logger.debug(f"task_director(): {item=}")
    task = TaskFactory(instance).create_task(task_name=item)
    logger.debug(f"task_director(): {task=}")
    if task is None:
        logger.error(f"Failed to resolve task: {item!r} — task returned None")
        return  # or raise an exception if desired
    try:
        task.perform_task()
    except AttributeError as err:
        logger.error(
            f"[AttributeError]: Task {item!r} is missing perform_task(): {err}"
        )
    except Exception as err:
        logger.exception(f"Unexpected error while executing {item!r}: {err}")


# Signed off by Brian Sanford on 20260116
