from dataclasses import dataclass, field

import build.tasks as tasks


@dataclass
class ADBSideloader(tasks.TaskFactoryTemplate):
    instance: type = field()
    comment: str = "Restart to verify build, then reboot to Bootloader"

    @property
    def index(self) -> int:
        return 2

    @property
    def title(self) -> str:
        return "Apply OTA Image"

    @property
    def command_string(self) -> str:
        return f"adb sideload {self.instance.path}"
