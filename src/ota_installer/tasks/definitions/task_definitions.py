# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterator
from dataclasses import dataclass, field

from ...decorators import ConfirmationPrompt, PaddedFooterWrapper
from ..mappings import TaskName

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
                TaskName.EXTRACT_PAYLOAD_IMAGE.lower_case,
                TaskName.RENAME_PAYLOAD_IMAGE.lower_case,
                TaskName.EXTRACT_STOCK_BOOT_IMAGE.lower_case,
                TaskName.BACKUP_STOCK_BOOT_IMAGE.lower_case,
            ]
        )


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                TaskName.CHECK_ADB_CONNECTION.lower_case,
                TaskName.PUSH_STOCK_BOOT_IMAGE.lower_case,
                TaskName.FIND_PATCHED_BOOT_IMAGE.lower_case,
                TaskName.PULL_PATCHED_BOOT_IMAGE.lower_case,
            ]
        )


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                TaskName.REBOOT_TO_RECOVERY.lower_case,
                TaskName.ADB_SIDELOAD.lower_case,
                TaskName.REBOOT_TO_BOOTLOADER.lower_case,
                TaskName.BOOT_MAGISK_IMAGE.lower_case,
            ]
        )
