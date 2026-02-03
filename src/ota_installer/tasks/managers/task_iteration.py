# src/ota_installer/tasks/managers/task_iteration.py
from types import NoneType

from ...decorators import StylizedIndentPrinter
from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from .task_director import task_director

StringTuple = tuple[str, ...]


def task_iterator(
    instance: VariableManager, task_group: StringTuple
) -> object | None:
    """Iterates over a task group and executes each task."""
    logger.debug(f"Iterating over task group: {task_group}")
    if not task_group:
        skipped_task_group_msg()
        return None

    for task in task_group:
        try:
            task_director(instance=instance, task_name=task)
        except TypeError as err:
            _handle_type_error(task_group, err)
        except Exception as err:
            logger.exception(f"TaskIteration Error: {err}")


def _handle_type_error(task_group: StringTuple, err: TypeError) -> None:
    """Handles TypeError exceptions during task iteration."""
    if isinstance(task_group, NoneType) or "NoneType" in str(err):
        skipped_task_group_msg()
    else:
        logger.error(f"TaskIteration Error: {err}")


@StylizedIndentPrinter(indent=2, style="variable", end="\n\n", use_output=True)
def skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"


# Signed off by Brian Sanford on 20260203
