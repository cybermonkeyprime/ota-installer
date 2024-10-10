from dataclasses import dataclass, field

import build.tasks as tasks


@dataclass
class ADBSideloader(tasks.TaskFactoryTemplate):
    instance: type = field()

    def __post_init__(self) -> None:
        try:
            self.index: int = 2
            self.title: str = "Apply OTA Image"
            self.command_string: str = f"adb sideload {self.instance.path}"
            self.comment: str = "Restart to verify build, then reboot to Bootloader"
        except AttributeError as e:
            raise ValueError("Invalid instance attribute ") from e
