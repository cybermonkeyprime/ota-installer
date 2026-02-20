# src/ota_installer/tasks/operations/task_operation_executor.py
from dataclasses import dataclass
from subprocess import CalledProcessError, check_output, run
from typing import Self

from ... import decorators
from ...log_setup import logger
from .constants.constants import Indents, Messages


@dataclass
class TaskOperationExecutor(object):
    """Executes shell commands with confirmation prompts and error handling."""

    command_string: str

    @decorators.ConfirmationPrompt(
        comment=Messages.EXECUTE.value,
        indent=Indents.EXECUTE,
        char=" ",
    )
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute(self) -> Self:
        """Executes the command without returning output."""
        try:
            run(self.command_string, shell=True, check=True)
        except CalledProcessError as error:
            logger.exception(
                f"Command failed with code {error.returncode}: {error.output}"
            )
        return self

    @decorators.ConfirmationPrompt(
        comment=Messages.EXECUTE.value,
        indent=Indents.EXECUTE,
        char=" ",
    )
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute_and_return_output(self, output_name) -> str:
        """Executes the command and returns its output."""
        try:
            result = (
                check_output(self.command_string, shell=True).decode().strip()
            )
        except CalledProcessError as error:
            logger.exception(
                f"{output_name} failed with code {error.returncode}: "
                f"{error.output}"
            )
            return ""
        return result


# Signed off by Brian Sanford on 20260209
