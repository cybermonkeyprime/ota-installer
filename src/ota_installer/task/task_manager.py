# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ..decorator.styled_indent_printer import StylizedIndentPrinter
from ..display.variable.processor.variable_process_handler import (
    ProcessorGroup,
)
from ..log_setup import add_structured_log_sink, logger
from ..variable.variable_manager import VariableManager
from .task_info import TaskID


@dataclass
class TaskManager:
    """Manages the execution of tasks based on a specified file name."""

    file_name: Path = field(default_factory=Path)
    function: Callable = field(default=type)
    # iteration: type = field(init=False)
    variable: VariableManager = field(init=False)

    def set_file_name(self, arguments) -> Self:
        """Sets the file name for the task manager."""
        self.file_name = Path(arguments)
        return self

    def set_variable(self) -> Self:
        """Initializes the variable manager and sets up logging."""
        from ..variable.variable_functions import set_variable_manager

        self.variable = set_variable_manager(self.file_name)
        if self.variable:
            add_structured_log_sink(self.variable.file_paths.log_file)

        if not self.variable:
            logger.error("Failed to initialize variable manager.")

        return self

    def set_posix_path(self) -> Self:
        """Sets the POSIX path for the file name."""
        self.posix_path = self.file_name
        return self

    def log_and_process_variables(self) -> None:
        """Logs and processes the variables from the variable manager."""
        logger.debug(
            f"TaskManager.log_and_process_variables(): {self.variable=}"
        )
        if not self.variable:
            logger.error("Variable manager is not initialized.")
        else:
            (
                ProcessorGroup.set_processor(self.variable)
                .process_directory_names()
                .process_file_names()
                .process_log_file()
            )

    def execute_iteration(self, task_group) -> None:
        """Executes the task iteration for the given task group."""
        task_iterator(instance=self.variable, task_group=task_group)


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
    return None


@StylizedIndentPrinter(indent=2, style="variable", end="\n\n", use_output=True)
def _skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"
