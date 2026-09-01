# src/ota_installer/task_group/task_group_director.py
from dataclasses import dataclass

from ..log_setup import logger
from ..task.task_director import TaskDirector, TaskInvocation
from .task_group_names import TaskGroupName


@dataclass(frozen=True, slots=True)
class TaskGroupDirector:
    task_director: TaskDirector
    dispatcher: TaskInvocation
    task_group: str | None = None

    @property
    def valid_group(self) -> bool:
        """Validates task group rules."""
        return bool(self.task_group) and self.dispatcher.contains(
            self.task_group
        )

    def execute(self) -> None:
        """Executes tasks based on the task group rules."""
        if self.valid_group:
            self.execute_single()
        else:
            self.execute_all()

    def execute_single(self) -> None:
        """Executes a single task if a task group is defined."""

        if not self.task_group:
            raise AttributeError(f"{self.task_group!r} does not exist!")

        logger.debug(
            f"Executing single task for task group: {self.task_group}"
        )
        self.task_director.execute(self.task_group)

    def execute_all(self) -> None:
        """Executes all tasks defined in the task group keys."""
        for task_group_key in TaskGroupName.get_task_group_members():
            self.task_director.execute(task_group_key)


# Signed off by Brian Sanford on 20260901
