# src/ota_installer/tasks/managers/task_manager.py
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Self

from ...display.variables.display_variable_processor import VariableProcessor
from ...log_setup import add_structured_log_sink, logger
from ...variables.functions import set_variable_manager
from ...variables.variable_manager import VariableManager
from .task_iteration import task_iterator


@dataclass
class TaskManager(object):
    """Manages the execution of tasks based on a specified file name."""

    file_name: Path = field(default_factory=Path)
    function: Callable = field(default=Callable)
    iteration: type = field(init=False)
    variable: VariableManager = field(init=False)

    def set_file_name(self, arguments) -> Self:
        """Sets the file name for the task manager."""
        self.file_name = Path(arguments)
        return self

    def set_variable(self) -> Self:
        """Initializes the variable manager and sets up logging.

        Returns:
            The updated TaskManager instance.
        """
        try:
            self.variable = set_variable_manager(self.file_name)
            add_structured_log_sink(self.variable.file_paths.log_file)

        except Exception as err:
            logger.exception(f"[{type(err).__name__}] {err}")
        return self

    def set_posix_path(self) -> Self:
        """Sets the POSIX path for the file name."""
        self.posix_path = self.file_name
        return self

    def list_vars(self) -> None:
        """Logs and processes the variables from the variable manager."""
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
        """Executes the task iteration for the given task group."""
        task_iterator(instance=self.variable, task_group=task_group)


