# src/ota_installer/tasks/managers/task_iteration.py
from types import NoneType

from ...decorators.styled_indent_printer import StylizedIndentPrinter
from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from ..constants.task_id import TaskID
from .task_director import task_director

StringTuple = tuple[str, ...]


def task_iterator(
    instance: VariableManager, task_group: StringTuple
) -> object | None:
    """Iterates over a task group and executes each task."""
    logger.debug(f"Iterating over task group: {task_group}")
    if not task_group:
        return _skipped_task_group_msg()

    for task_name in task_group:
        task_id = TaskID(task_name)
        task_class = task_id.execute

        task_director(instance=instance, task_name=task_class)


@StylizedIndentPrinter(indent=2, style="variable", end="\n\n", use_output=True)
def _skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"


