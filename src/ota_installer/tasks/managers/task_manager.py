# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ...display import VariableProcessor
from ...log_setup import logger
from ...variables import VariableManager
from .task_iteration import TaskIteration


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
