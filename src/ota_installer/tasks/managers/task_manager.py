# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from types import NoneType
from typing import Self

from ...decorators import StylizedIndentPrinter
from ...display import VariableProcessor
from ...log_setup import logger
from ...variables import VariableManager
from ..factories import TaskFactory

StringTuple = tuple[str, ...]


@dataclass
class TaskIteration(object):
    """Represents an iteration of tasks to be executed."""

    instance: VariableManager = field()
    task_group: StringTuple = field(default=("", ""))

    def execute_iteration(self, task_group: StringTuple) -> object | None:
        task_director = TaskDirector()
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


@dataclass
class TaskManager(object):
    """Manages the execution of tasks based on a file name."""

    file_name: Path = field(default_factory=Path)
    function: Callable = field(default=Callable)
    iteration: TaskIteration = field(init=False)
    variable: VariableManager = field(init=False)

    def set_file_name(self, arguments) -> Self:
        self.file_name = Path(arguments)
        return self

    def set_variable(self) -> Self:
        try:
            self.variable = VariableManager(self.file_name)
        except Exception as err:
            print(f"[{type(err).__name__}] {err}")
        return self

    def set_iteration(self) -> Self:
        self.iteration = TaskIteration(self.variable)
        return self

    def set_posix_path(self) -> Self:
        self.posix_path = self.file_name
        return self

    def list_vars(self) -> None:
        try:
            (
                VariableProcessor(self.variable)
                .process_directory_names()
                .process_file_names()
                .process_log_file()
            )
        except Exception as err:
            logger.exception(f"list_vars: {type(err).__name__} {err}")

    def execute_iteration(self, task_group) -> None:
        self.iteration.execute_iteration(task_group)


@dataclass
class TaskDirector(object):
    """Manages the initiation of task processing."""

    def handle_task(self, instance: VariableManager, item: str) -> None:
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
