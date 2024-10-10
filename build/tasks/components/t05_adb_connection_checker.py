from dataclasses import dataclass, field

import build.tasks as tasks
import build.variables as variables


@dataclass
class ADBConnectionChecker(tasks.TaskFactoryTemplate):
    instance: type[variables.Manager] = field(default=variables.Manager)

    def __post_init__(self) -> None:
        self.index: int = 1
        self.title: str = "Check ADB Connection"
        self.command_string: str = "adb devices"
