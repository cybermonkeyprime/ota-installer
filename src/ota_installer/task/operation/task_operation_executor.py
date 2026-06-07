# src/ota_installer/tasks/operations/task_operation_executor.py
from dataclasses import dataclass
from functools import partial
from subprocess import check_output, run
from typing import Self

from ... import decorator
from ...log_setup import logger
from .task_operation_info import Indents, Messages


@dataclass(frozen=True, slots=True)
class Task:
    prompt = partial(
        decorator.ConfirmationPrompt,
        comment=Messages.EXECUTE.value,
        indent=Indents.EXECUTE,
    )
    on_keypress = partial(
        decorator.ContinueOnKeyPress,
        indent=1,
    )


@dataclass
class TaskOperationExecutor:
    """Executes shell commands with confirmation prompts and error handling."""

    command: str

    @Task.prompt()
    @Task.on_keypress()
    @decorator.Encapsulate()
    def execute(self) -> Self:
        """Executes the command without returning output."""
        if run(args=self.command, shell=True, check=True).returncode != 0:
            logger.exception(f"Command execution failed: {self.command}")
        return self

    @Task.prompt()
    @Task.on_keypress()
    @decorator.Encapsulate()
    def execute_and_return_output(self, output_name) -> str:
        """Executes the command and returns its output."""
        try:
            result = check_output(self.command, shell=True, text=True).strip()
        except Exception as e:
            logger.exception(
                f"{output_name} execution failed: {self.command} - {e}"
            )
            return ""
        return result
