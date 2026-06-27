# src/ota_installer/tasks/operations/task_operation_executor.py
from dataclasses import dataclass
from enum import StrEnum
from functools import partial
from subprocess import check_output, run
from typing import Self

from ... import decorator
from ...log_setup import logger
from .task_operation_info import Indents, Messages


class TaskType(StrEnum):
    EXECUTE = Messages.EXECUTE.value
    OUTPUT = ""


@dataclass(frozen=True, slots=True)
class Task:
    prompt = partial(
        decorator.ConfirmationPrompt,
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

    @Task.prompt(TaskType.EXECUTE)
    @Task.on_keypress()
    @decorator.Encapsulate()
    def execute(self) -> Self:
        """Executes the command without returning output."""
        if run(args=self.command, shell=True, check=True).returncode != 0:
            logger.exception(f"Command execution failed: {self.command}")
        return self

    @Task.prompt(TaskType.OUTPUT)
    @Task.on_keypress()
    @decorator.Encapsulate()
    def execute_and_return_output(self, output_name) -> str:
        """Executes the command and returns its output."""
        result = (
            check_output(self.command, shell=True, text=True).strip()
            if self.command
            else ""
        )
        if not result:
            logger.exception(f"{output_name} execution failed: {self.command}")
        return result


# Signed off by Brian Sanford on 20260626
