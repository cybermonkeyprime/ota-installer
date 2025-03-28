from collections.abc import Iterator
from dataclasses import dataclass, field

from decorators import ConfirmationPrompt, PaddedFooterWrapper


@dataclass
class TaskDefinitions:
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
class TaskDefinitionsTemplate:
    _tasks: tuple[str, ...] = field(default_factory=tuple)

    @property
    def tasks(self) -> tuple[str, ...]:
        return self._tasks

    @tasks.setter
    def tasks(self, value: tuple[str, ...]) -> None:
        self._tasks = value

    def __iter__(self) -> Iterator[str]:
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


def main() -> bool:
    @PaddedFooterWrapper()
    @ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def preparation() -> "PreparationTaskDefinitions":
        return PreparationTaskDefinitions()

    preparation()
    return True


if __name__ == "__main__":
    main()
