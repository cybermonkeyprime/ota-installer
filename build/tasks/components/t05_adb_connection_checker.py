from dataclasses import dataclass, field

from build.tasks import TaskFactoryTemplate
from build.variables import VariableManager


@dataclass
class ADBConnectionChecker(TaskFactoryTemplate):
    """
    A class to check ADB (Android Debug Bridge) connection status.

    Attributes:
        variable_manager (Type[VariableManager]): The variable manager instance.
        task_index (int): The index of the task.
        task_title (str): The title of the task.
        command_string (str): The ADB command to check the connection.
    """

    variable_manager: "type[VariableManager]" = field(default=VariableManager)
    index: int = 1
    title: str = "Check ADB Connection"

    command_string: str = "adb devices"
