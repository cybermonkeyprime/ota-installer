# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field

from loguru import logger

from ...decorators import ConfirmationPrompt, PaddedFooterWrapper
from ...task_groups.constants.application_tasks import (
    ApplicationTasks,
)
from ...task_groups.constants.migration_tasks import (
    MigrationTasks,
)
from ...task_groups.constants.preparation_tasks import (
    PreparationTasks,
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


def enum_name_list(enum: Iterable) -> list:
    result = [enum_member.value.value for enum_member in enum]
    logger.debug(result)
    return result


@dataclass
class PreparationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_name_list(PreparationTasks))


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_name_list(MigrationTasks))


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_name_list(ApplicationTasks))
