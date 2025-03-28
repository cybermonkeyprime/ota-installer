from dataclasses import dataclass, field

import build.tasks as tasks
import build.variables as variables


@dataclass
class ADBConnectionChecker(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 1

    @property
    def title(self) -> str:
        return "Check ADB Connection"

    @property
    def command_string(self) -> str:
        return "adb devices"
