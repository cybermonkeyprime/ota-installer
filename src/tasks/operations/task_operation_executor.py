from dataclasses import dataclass
from subprocess import CalledProcessError, check_output, run
from typing import Self

from src import decorators

from .constants import ExecutorConstants


@dataclass
class TaskOperationExecutor(object):
    command_string: str

    @decorators.ConfirmationPrompt(
        comment=ExecutorConstants.MESSAGE.value,
        indent=ExecutorConstants.INDENT.value,
        char=" ",
    )
    @decorators.ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute(self) -> Self:
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
        result = check_output(self.command_string, shell=True).decode().strip()
        print(f"{output_name} = {result}")
        return result
