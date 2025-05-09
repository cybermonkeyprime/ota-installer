from dataclasses import dataclass
from pathlib import Path
from typing import Union


@dataclass
class Test(object):
    path: Path = Path("/Bob/Jr/sample.zip")


@dataclass
class TaskDictionary(object):
    instance: type

    type ItemDictionary = dict[str, Union[int, str, None]]

    @property
    def task_dictionary(self) -> "dict[str, ItemDictionary]":
        return dict(
            payload_image_extractor=self.payload_image_extractor,
            adb_connection_checker=self.adb_connection_checker,
            magisk_image_booter=self.magisk_image_booter,
        )

    @property
    def payload_image_extractor(self) -> "ItemDictionary":
        return dict(
            index=1,
            title="Payload Image Extracter",
            command=f"unzip -o {self.instance.path} payload.bin -d {Path.home()}",
            comment=None,
        )

    @property
    def adb_connection_checker(self) -> "ItemDictionary":
        return dict(
            index=1,
            title="Check ADB Connection",
            commant="adb devices",
            comment=None,
        )

    @property
    def magisk_image_booter(self) -> "ItemDictionary":
        return dict(
            index=4,
            title="Boot to Magisk Image",
            command="fastboot",
            comment="Enjoy",
        )

    def fetch_values(self, task_string) -> dict:
        return self.task_dictionary[task_string]


def main() -> None:
    test = Test
    td = TaskDictionary(test)
    for task in td.task_dictionary:
        index, header, command, comment = [*td.fetch_values(task).values()]
        print(
            f"{index}. {header} | {command} | {comment if comment else 'N/A'}"
        )


if __name__ == "__main__":
    main()
