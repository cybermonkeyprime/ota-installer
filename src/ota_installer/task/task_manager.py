# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import SimpleNamespace
from typing import Self

from ota_installer.plugin.plugin_registry import Plugin

from ..display.display_variable_info import (
    DisplayVariablePipeline,
)
from ..log_setup import add_structured_log_sink, logger
from ..style import decorator
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
            logger.error(
                f"Failed to initialize {type(self.variable).__name__}"
            )

        return self

    def set_posix_path(self) -> Self:
        """Sets the POSIX path for the file name."""
        self.posix_path = self.file_name
        return self

    def log_and_process_variables(self) -> None:
        """Logs and processes the variables from the variable manager."""
        log_api = {
            "debug": f"TaskManager.log_and_process_variables(): {self.variable=}",
            "error": "Variable manager is not initialized.",
        }

        log_obj = SimpleNamespace(**log_api)

        logger.debug(log_obj.debug)

        if self.variable:
            (
                DisplayVariablePipeline(self.variable)
                .process_directory_names()
                .process_file_names()
            )
        else:
            logger.error(log_obj.error)

    def execute_iteration(self, task_group) -> None:
        """Executes the task iteration for the given task group."""
        task_pipeline(instance=self.variable, task_group=task_group)


@dataclass(frozen=True, slots=True)
class TaskDirectorRender:
    cls: Callable
    arguments: dict | None

    def run(self):
        arguments = self.arguments if self.arguments is not None else {}
        return self.cls(**arguments)


def task_director(instance: VariableDirector, task_name: Callable) -> None:
    """Manages the initiation of task processing."""
    logger.debug(f"Initiating task: {task_name}")
    task = task_name(instance=instance)

    class TaskDirectorError(Enum):
        LOGGER = TaskDirectorRender(
            logger.error,
            {
                "message": f"Task {task_name!r} is missing perform_task() method."
            },
        )
        VALUE = TaskDirectorRender(
            ValueError,
            {
                "message": f"Task {task_name!r} is not executable.",
            },
        )

        def run(self):
            self.value.run()

    if not _is_executable(task):
        TaskDirectorError.LOGGER.run()
        raise TaskDirectorError.VALUE.run()

    task.perform_task()


def _is_executable(task: object) -> bool:
    """Checks if the task has a perform_task method."""
    return callable(getattr(task, "perform_task", None))


StringTuple = tuple[str, ...]


def task_pipeline(instance: VariableDirector, task_group: StringTuple) -> str:
    """Iterates over a task group and executes each task."""

    logger.debug(f"Iterating over task group: {task_group}")

    if not task_group:
        return _skipped_task_group_msg()

    run_invocator = TaskInvocation

    task_classes = tuple(Plugin.TASK[name] for name in task_group)

    for task_class in task_classes:
        api = {
            "arguments": {"instance": instance, "task_name": task_class},
        }

        api_obj = SimpleNamespace(**api)
        arguments = SimpleNamespace(**api_obj.arguments)

        if callable(task_class):
            logger.debug(f"{arguments.task_name}")
            run_invocator(**api_obj.arguments).run()
    return ""


@dataclass(frozen=True)
class TaskInvocation:
    instance: VariableDirector
    task_name: type

    def run(self):
        task_director(
            instance=self.instance,
            task_name=self.task_name,
        )


@decorator.StylizedIndentPrinter(
    indent=2, style="variable", end="\n\n", use_output=True
)
def _skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"


# Signed off by Brian Sanford on 20260702
