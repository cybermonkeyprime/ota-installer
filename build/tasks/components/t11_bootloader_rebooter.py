from dataclasses import dataclass

import build.tasks as tasks


@dataclass
class BootloaderRebooter(tasks.TaskFactoryTemplate):
    instance: type

    def __post_init__(self) -> None:
        self.index: int = 3
        self.title: str = "Reboot to Bootloader"
        self.command_string: str = "adb reboot bootloader"
