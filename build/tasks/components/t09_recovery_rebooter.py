from dataclasses import dataclass, field

import build.tasks as tasks


@dataclass
class RecoveryRebooter(tasks.TaskFactoryTemplate):
    instance: type = field(default=tasks.TaskFactoryTemplate)

    def __post_init__(self) -> None:
        self.index: int = 1
        self.title: str = "Reboot to Recovery"
        self.command_string: str = "adb reboot recovery"
