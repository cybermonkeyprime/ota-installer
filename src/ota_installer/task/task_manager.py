# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from types import SimpleNamespace
from typing import Self

from ..display.display_variables import (
    DisplayVariablePipeline,
)
from ..log_setup import add_structured_log_sink, logger
from ..plugin.plugin_registry import Plugin
from ..style import decorator
from ..variable.variable_director import VariableDirector


@dataclass
class TaskManager:
    """Manages the execution of tasks based on a specified file name."""

    file_name: Path = field(default_factory=Path)
    variable: VariableDirector = field(init=False)

    def set_file_name(self, arguments: Path) -> Self:
        """Sets the file name for the task manager."""
        self.file_name = Path(arguments)
        return self

    def set_variable(self) -> Self:
        """Initializes the variable manager and sets up logging."""
        from ..variable.variable_director import variable_pipeline

        self.variable = variable_pipeline(self.file_name)
        if self.variable:
            add_structured_log_sink(self.variable.file_paths.log_file)
        else:
            logger.error(
                f"Failed to initialize {type(self.variable).__name__}"
            )

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

    def execute_iteration(self, pipeline: Pipeline) -> None:
        pipeline.run(self.variable)


@dataclass(frozen=True, slots=True)
class Pipeline:
    stages: tuple[str, ...] | None

    def run(self, context: VariableDirector) -> None:
        if self.stages is None:
            _skipped_task_group_msg()
            return

        for stage in self.stages:
            task_class = Plugin.TASK[stage]

            task_director(
                instance=context,
                task_name=task_class,
            )


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


@decorator.StylizedIndentPrinter(
    indent=2, style="variable", end="\n\n", use_output=True
)
def _skipped_task_group_msg() -> str:
    """Displays a message indicating that the task group was skipped."""
    return "Task Group skipped"


# Signed off by Brian Sanford on 20260702
