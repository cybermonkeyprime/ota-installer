from dataclasses import dataclass, field
from subprocess import CalledProcessError, check_output

from decorators import (
    ConfirmationPrompt,
    ContinueOnKeyPress,
)

import build.decorators as decorators
import build.tasks as tasks
import build.variables as variables


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
    def magisk_remote_path(self) -> type:
        return self.instance.directory.magisk_image_path.remote_path

    @property
    def command_string(self) -> str:
        return f"adb shell ls {self.magisk_remote_path}/magisk_patched*.img | head -n1"

    @ConfirmationPrompt(comment="Execute the command", indent=2, char=" ")
    @ContinueOnKeyPress(indent=1, char=" ")
    @decorators.Encapsulate()
    def execute_command_string(self) -> None:
        try:
            result = check_output([self.command_string], shell=True).decode()
            print(f"{4 * ' '}Patched Boot Image = {result}")
            self.instance.patched_image_name = result
        except CalledProcessError as e:
            print(f"An error occurred while executing the command: {e}")
