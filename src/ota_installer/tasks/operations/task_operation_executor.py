# src/ota_installer/tasks/operations/task_operation_executor.py
from dataclasses import dataclass
from subprocess import CalledProcessError, check_output, run
from typing import Self

from ... import decorators
from .constants.constants import ExecutorConstants


@dataclass
class TaskOperationExecutor(object):
    """
    Executes shell commands with confirmation prompts and error handling.
    """

    command_string: str

    @decorators.ConfirmationPrompt(
        comment=ExecutorConstants.MESSAGE.value,
        indent=ExecutorConstants.INDENT.value,
        char=" ",
    )
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute(self) -> Self:
        """Executes the command without returning output."""
        try:
            run([self.command_string], shell=True, check=True)
        except CalledProcessError:
            pass
        return self

    @decorators.ConfirmationPrompt(
        comment=ExecutorConstants.MESSAGE.value,
        indent=ExecutorConstants.INDENT.value,
        char=" ",
    )
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute_and_return_output(self, output_name) -> str:
        """Executes the command and returns its output."""
        result = (
            check_output(self.command_string.split(), shell=True)
            .decode()
            .strip()
        )
        print(f"{output_name} = {result}")
        return result


# Signed off by Brian Sanford on 20260119
