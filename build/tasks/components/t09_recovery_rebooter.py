from dataclasses import dataclass, field

import build.tasks as tasks


@dataclass
class RecoveryRebooter(tasks.TaskFactoryTemplate):
    instance: type = field(default=tasks.TaskFactoryTemplate)

    @property
    def index(self) -> int:
        return 1

    @property
    def title(self) -> str:
        return "Reboot to Recovery"

    @property
    def command_string(self) -> str:
        return "adb reboot recovery"
