# src/ota_installer/tasks/managers/task_director.py
from dataclasses import dataclass

from ...log_setup import logger
from ...variables import VariableManager
from ..factories import TaskFactory


@dataclass
class TaskDirector(object):
    """Manages the initiation of task processing."""

    def handle_task(self, instance: VariableManager, item: str) -> None:
        logger.debug(item)
        task = TaskFactory(instance).create_task(task_name=item)
        if task is None:
            logger.error(
                f"Failed to resolve task: {item!r} — task returned None"
            )
            return  # or raise an exception if desired
        try:
            task.perform_task()
        except AttributeError as err:
            logger.error(
                f"[AttributeError]: Task {item!r} is missing perform_task(): {err}"
            )
        except Exception as err:
            logger.exception(
                f"Unexpected error while executing {item!r}: {err}"
            )


def task_director(instance: VariableManager, item: str) -> None:
    """Manages the initiation of task processing."""
    logger.debug(item)
    task = TaskFactory(instance).create_task(task_name=item)
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
