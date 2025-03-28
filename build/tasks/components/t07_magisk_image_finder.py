from dataclasses import dataclass, field
from subprocess import CalledProcessError, check_output

import build.variables as variables
import build.tasks as tasks

from decorators import (
    ContinueOnKeyPress,
    ConfirmationPrompt,
)

import build.decorators as decorators


@dataclass
class MagiskImageFinder(tasks.TaskFactoryTemplate):
    instance: type = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 3

    @property
    def title(self) -> str:
        return "Find Magisk Image"

    @property
    def command_string(self) -> str:
        return f"adb shell ls { self.instance.directory.magisk_image.remote_path} | grep magisk_patched | head -n1"

    @ConfirmationPrompt(comment="Execute the command", indent=2, char=" ")
    @ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute_command_string(self) -> None:
        try:
            result = check_output(self.command_string, shell=True).decode().strip("\n")
            print(f"{4 * " "}Patched Boot Image = {result}")
            self.instance.patched_image_name = result
        except CalledProcessError as e:
            print(f"An error occurred while executing the command: {e}")
