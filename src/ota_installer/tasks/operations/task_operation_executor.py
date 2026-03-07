# src/ota_installer/tasks/operations/task_operation_executor.py
from dataclasses import dataclass
from functools import partial
from subprocess import check_output, run
from typing import Self

from ... import decorators
from ...log_setup import logger
from .constants.constants import Indents, Messages


@dataclass(frozen=True, slots=True)
class Task(object):
    prompt = partial(
        decorators.ConfirmationPrompt,
        comment=Messages.EXECUTE.value,
        indent=Indents.EXECUTE,
    )
    on_keypress = partial(
        decorators.ContinueOnKeyPress,
        indent=1,
    )


@dataclass
class TaskOperationExecutor(object):
    """Executes shell commands with confirmation prompts and error handling."""

    command_string: str

    @Task.prompt()
    @Task.on_keypress()
    @decorators.Encapsulate()
    def execute(self) -> Self:
        """Executes the command without returning output."""
        if run(self.command_string, shell=True, check=True).returncode != 0:
            logger.exception(
                f"Command execution failed: {self.command_string}"
            )
        return self

    @Task.prompt()
    @Task.on_keypress()
    @decorators.Encapsulate()
    def execute_and_return_output(self, output_name) -> str:
        """Executes the command and returns its output."""
        result = check_output(
            self.command_string, shell=True, text=True
        ).strip()
        if result is None:
            logger.exception(
                f"{output_name} execution failed: {self.command_string}"
            )
            return ""
        return result
