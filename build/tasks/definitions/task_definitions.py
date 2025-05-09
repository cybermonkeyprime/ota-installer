from collections.abc import Iterator
from dataclasses import dataclass, field

from decorators import ConfirmationPrompt, PaddedFooterWrapper

from build.tasks.task_questions import TaskGroupQuestions


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

    tasks: "tuple[str, ...]" = field(default_factory=tuple)

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

    task_group_questions: "type" = TaskGroupQuestions

    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        question=task_group_questions.PREPARATION.value,
        confirmation_char=" ",
    )
    def preparation(self) -> "PreparationTaskDefinitions":
        return PreparationTaskDefinitions()

    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        question=task_group_questions.MIGRATION.value,
        confirmation_char=" ",
    )
    def migration(self) -> "MigrationTaskDefinitions":
        return MigrationTaskDefinitions()

    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        question=task_group_questions.APPLICATION.value,
        confirmation_char=" ",
    )
    def application(self) -> "ApplicationTaskDefinitions":
        return ApplicationTaskDefinitions()


def main() -> None:
    pass


if __name__ == "__main__":
    main()
