# src/ota_installer/tasks/managers/task_manager.py
import sys
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ...display import VariableProcessor
from ...log_setup import add_structured_log_sink, logger
from ...variables import VariableManager
from .task_iteration import TaskIteration, task_iterator


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
            from ...validation.file_path_validation import file_path_validator

            valid_path = file_path_validator(self.file_name)
            if not valid_path:
                logger.error(f"Invalid file path: {self.file_name}")
                sys.exit("Invalid input file. Aborting.")
            self.variable = VariableManager(valid_path)
            add_structured_log_sink(self.variable.file_paths["log_file"])

        except Exception as err:
            logger.exception(f"[{type(err).__name__}] {err}")
        return self

    def set_posix_path(self) -> Self:
        self.posix_path = self.file_name
        return self

    def list_vars(self) -> None:
        logger.debug(f"TaskManager.list_vars(): {self.variable=}")
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
        task_iterator(instance=self.variable, task_group=task_group)
        # self.iteration.execute_iteration(task_group)
