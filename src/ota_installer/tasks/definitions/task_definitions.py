# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field

from loguru import logger

from ... import decorators
from ...task_groups.constants.application_tasks import (
    ApplicationTasks,
)
from ...task_groups.constants.migration_task import (
    MigrationTask,
)
from ...task_groups.constants.preparation_tasks import (
    PreparationTasks,
)

StrTuple = tuple[str, ...]
StrIterator = Iterator[str]


@dataclass
class TaskDefinitions(object):
    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def preparation(self) -> "PreparationTaskDefinitions":
        return PreparationTaskDefinitions()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Migration Tasks", char=" "
    )
    def migration(self) -> "MigrationTaskDefinitions":
        return MigrationTaskDefinitions()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Application Tasks", char=" "
    )
    def application(self) -> "ApplicationTaskDefinitions":
        return ApplicationTaskDefinitions()


@dataclass
class TaskDefinitionsTemplate(object):
    tasks: StrTuple = field(default_factory=tuple)

    def __iter__(self) -> StrIterator:
        return iter(self.tasks)


def enum_task_names(enum: Iterable) -> list:
    result = [enum_member.value.value for enum_member in enum]
    logger.debug(f"enum_task_names(): {result=}")
    return result


@dataclass
class PreparationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_task_names(PreparationTasks))


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_task_names(MigrationTask))


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    def __post_init__(self) -> None:
        self.tasks = tuple(enum_task_names(ApplicationTasks))
