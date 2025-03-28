from dataclasses import dataclass, field

import build.tasks as tasks
import build.variables as variables


@dataclass
class BootloaderRebooter(tasks.TaskFactoryTemplate):
    instance: type[variables.VariableManager] = field(default=variables.VariableManager)

    @property
    def index(self) -> int:
        return 3

    @property
    def title(self) -> str:
        return "Reboot to Bootloader"

    @property
    def command_string(self) -> str:
        return "adb reboot bootloader"
