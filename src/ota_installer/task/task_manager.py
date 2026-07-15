# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ota_installer.plugin.plugin_registry import TASK_PLUGINS

from ..decorator.styled_indent_printer import StylizedIndentPrinter
from ..display.display_variable_info import (
    DisplayVariablePipeline,
)
from ..log_setup import add_structured_log_sink, logger
from ..variable.variable_director import VariableDirector


@dataclass
class TaskManager:
    """Manages the execution of tasks based on a specified file name."""

    file_name: Path = field(default_factory=Path)
    function: Callable = field(default=type)
    variable: VariableDirector = field(init=False)

    def set_file_name(self, arguments: Path) -> Self:
        """Sets the file name for the task manager."""
        self.file_name = Path(arguments)
        return self

    def set_variable(self) -> Self:
        """Initializes the variable manager and sets up logging."""
        from ..variable.set_variable_director import set_variable_director

        self.variable = set_variable_director(self.file_name)
        if self.variable:
            add_structured_log_sink(self.variable.file_paths.log_file)
        else:
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
        if self.variable:
            (
                DisplayVariablePipeline(self.variable)
                .process_directory_names()
                .process_file_names()
            )
        else:
            logger.error("Variable manager is not initialized.")

    def execute_iteration(self, task_group) -> None:
        """Executes the task iteration for the given task group."""
        task_pipeline(instance=self.variable, task_group=task_group)


def task_director(instance: VariableDirector, task_name: Callable) -> None:
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


def task_pipeline(instance: VariableDirector, task_group: StringTuple) -> str:
    """Iterates over a task group and executes each task."""

    logger.debug(f"Iterating over task group: {task_group}")

    if not task_group:
        return _skipped_task_group_msg()

    run_director = task_director
    get_plugin = TASK_PLUGINS

    task_classes = (get_plugin[name] for name in task_group)

    for task_class in task_classes:
        if callable(task_class):
            run_director(instance=instance, task_name=task_class)
    return ""


@StylizedIndentPrinter(indent=2, style="variable", end="\n\n", use_output=True)
def _skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"


# Signed off by Brian Sanford on 20260702
