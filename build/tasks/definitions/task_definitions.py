from collections.abc import Iterator
from typing import Callable, Tuple
from dataclasses import dataclass, field

from decorators import ConfirmationPrompt, PaddedFooterWrapper

StrTuple = Tuple[str, ...]

@dataclass
class TaskDefinition(object):
    """
    A base class for task definitions.
    """
    pass


@dataclass
class TaskDefinitionSequence(TaskDefinition):
    """
    A class representing a sequence of tasks.
    """
    tasks: Tuple[str, ...] = field(default_factory=tuple)

    def __iter__(self) -> Iterator[str]:
        return iter(self.tasks)



@dataclass
class PreparationTaskDefinitions(TaskDefinitionSequence):
    """
    A class representing preparation tasks.
    """
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
class MigrationTaskDefinitions(TaskDefinitionSequence):
    """
    A class representing migration tasks.
    """
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
class ApplicationTaskDefinitions(TaskDefinitionSequence):
    """
    A class representing application tasks.
    """
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [
                "reboot_to_recovery",
                "adb_sideload",
                "reboot_to_bootloader",
                "boot_magisk_image",
            ]
        )

@dataclass
class TaskDefinitions(object):
    """
    A class to manage task sequences.
    """
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

    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def perform_preparation_tasks(self) -> Callable:
        return self.preparation

    @PaddedFooterWrapper()
    @ConfirmationPrompt(comment="perform the Migration Tasks", char=" ")
    def perform_migration_tasks(self) -> Callable:
        return self.migration

    @PaddedFooterWrapper()
    @ConfirmationPrompt(comment="perform the Application Tasks", char=" ")
    def perform_application_tasks(self) -> Callable:
        return self.application

def main() -> None:
    task_definitions = TaskDefinitions(
    )

    task_definitions.perform_preparation_tasks()
    task_definitions.perform_migration_tasks()
    task_definitions.perform_application_tasks()

if __name__ == "__main__":
    main()
