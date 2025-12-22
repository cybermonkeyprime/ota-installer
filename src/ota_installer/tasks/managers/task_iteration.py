# src/ota_installer/tasks/managers/task_manager.py
from dataclasses import dataclass, field
from types import NoneType

from ...decorators import StylizedIndentPrinter
from ...log_setup import logger
from ...variables import VariableManager
from .task_director import TaskDirector

StringTuple = tuple[str, ...]


@dataclass
class TaskIteration(object):
    """Represents an iteration of tasks to be executed."""

    instance: VariableManager = field()
    task_group: StringTuple = field(default=("", ""))

    def execute_iteration(self, task_group: StringTuple) -> object | None:
        task_director = TaskDirector()
        logger.debug(task_group)
        try:
            stack = list(task_group)
            handle_task = task_director.handle_task
            for task in stack:
                handle_task(instance=self.instance, item=task)
        except TypeError as err:
            # Check if this is likely due to a NoneType or signature mismatch
            if isinstance(task_group, NoneType) or "NoneType" in str(err):
                skipped_task_group_msg()
            else:
                logger.error(
                    f"[{type(err).__name__}] TaskIteration Error: {err}"
                )
            pass
        except Exception as err:
            logger.exception(
                f"[{type(err).__name__}] TaskIteration Error: {err}"
            )


@StylizedIndentPrinter(indent=2, style="variable", end="\n\n", use_output=True)
def skipped_task_group_msg() -> str:
    return "Task Group skipped"
