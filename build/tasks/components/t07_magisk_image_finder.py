from dataclasses import dataclass, field
from subprocess import CalledProcessError, check_output

from build.decorators import (
    ConfirmationPrompt,
    ContinueOnKeyPress,
    Encapsulate,
)
from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class MagiskImageFinder(TaskFactoryTemplate):
    """
    A class responsible for finding the Magisk patched boot image on a remote path.

    Attributes:
        variable_manager: An instance of VariableManager to manage paths.
    """

    variable_manager: "type[VariableManager]" = field(default=VariableManager)
    index: int = 3
    title: str = "Find Magisk Image"

    @property
    def magisk_remote_path(self) -> type:
        return self.variable_manager.directory.magisk_image_path.remote_path

    @property
    def command_string(self) -> str:
        """Constructs the command string to find the Magisk patched boot image."""
        return f"adb shell ls {self.magisk_remote_path}/magisk_patched*.img | head -n1"

    @ConfirmationPrompt(
        question="Execute the command",
        indentation_level=2,
        confirmation_char=" ",
    )
    @ContinueOnKeyPress(indent=1, char=" ")
    @Encapsulate()
    def execute_command_string(self) -> None:
        """Executes the command string to find the Magisk patched boot image."""
        try:
            result = check_output([self.command_string], shell=True).decode()
            print(f"{4 * ' '}Patched Boot Image = {result}")
            self.variable_manager.patched_image_name = result
        except CalledProcessError as e:
            print(f"An error occurred while executing the command: {e}")


if __name__ == "__main__":
    # Dependency injection example
    magisk_finder = MagiskImageFinder()
    magisk_finder.execute_command_string()
