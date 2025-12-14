# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterator
from dataclasses import dataclass, field

from ...decorators import ConfirmationPrompt, PaddedFooterWrapper

StrTuple = tuple[str, ...]
StrIterator = Iterator[str]


@dataclass
class TaskDefinitions(object):
    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def preparation(self) -> "PreparationTaskDefinitions":
        return PreparationTaskDefinitions()

    @PaddedFooterWrapper()
    @ConfirmationPrompt(comment="perform the Migration Tasks", char=" ")
    def migration(self) -> "MigrationTaskDefinitions":
        return MigrationTaskDefinitions()

    @PaddedFooterWrapper()
    @ConfirmationPrompt(comment="perform the Application Tasks", char=" ")
    def application(self) -> "ApplicationTaskDefinitions":
        return ApplicationTaskDefinitions()


@dataclass
class TaskDefinitionsTemplate(object):
    _tasks: StrTuple = field(default_factory=tuple)

    @property
    def tasks(self) -> StrTuple:
        return self._tasks

    @tasks.setter
    def tasks(self, value: StrTuple) -> None:
        self._tasks = value

    def __iter__(self) -> StrIterator:
        return iter(self._tasks)


@dataclass
class PreparationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                "extract_payload_image",
                "rename_payload_image",
                "extract_stock_boot_image",
                "backup_stock_boot_image",
            ]
        )


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                "check_adb_connection",
                "push_stock_boot_image",
                "find_patched_boot_image",
                "pull_patched_boot_image",
            ]
        )


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                "reboot_to_recovery",
                "adb_sideload",
                "reboot_to_bootloader",
                "boot_magisk_image",
            ]
        )
