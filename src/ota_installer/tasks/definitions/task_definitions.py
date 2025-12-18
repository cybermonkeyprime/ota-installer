# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterator
from dataclasses import asdict, dataclass, field

from ...decorators import ConfirmationPrompt, PaddedFooterWrapper
from ..mappings.constants import (
    ApplicationTasks,
    MigrationTasks,
    PreparationTasks,
    TaskName,
)

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
            [enum_member.value for enum_member in PreparationTasks]
        )


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [enum_member.value for enum_member in MigrationTasks]
        )


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(
            [enum_member.value for enum_member in ApplicationTasks]
        )
