#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Union
from pathlib import Path


@dataclass
class Test(object):
    path: Path = Path("/Bob/Jr/sample.zip")


@dataclass
class TaskDictionary(object):
    instance: type

    def __post_init__(self) -> None:
        self.task_dictionary: dict[str, dict[str, Union[int, str, None]]] = dict(
            payload_image_extractor=dict(
                index=1,
                title="Payload Image Extracter",
                command=f"unzip -o {self.instance.path} payload.bin -d {Path.home()}",
                comment=None,
            ),
            # payload_image_renamer=TaskAttributes(2, "", ""),
            # boot_image_extractor=TaskAttributes(3, "", ""),
            # stock_boot_backupper=TaskAttributes(4, "", ""),
            adb_connection_checker=dict(
                index=1,
                title="Check ADB Connection",
                commant="adb devices",
                comment=None,
            ),
            # stock_boot_image_pusher=TaskAttributes(2, "", ""),
            # magisk_image_finder=TaskAttributes(3, "", ""),
            # magisk_image_puller=TaskAttributes(4, "", ""),
            # recovery_rebooter=TaskAttributes(1, "header", "adb reboot recovery",),
            # apply_ota_updater=TaskAttributes(2, "header", "command","comment"),
            # bootloader_rebooter=TaskAttributes(3, "header", "adb reboot bootloader",""),
            magisk_image_booter=dict(
                index=4,
                title="Boot to Magisk Image",
                command="fastboot",
                comment="Enjoy",
            ),
        )

    def fetch_values(self, task_string) -> dict:
        return self.task_dictionary[task_string]


def main() -> None:
    test = Test
    td = TaskDictionary(test)
    for task in td.task_dictionary:
        index, header, command, comment = [*td.fetch_values(task).values()]
        print(f"{index}. {header} | {command} | {comment if comment else "N/A"}")


if __name__ == "__main__":
    main()
