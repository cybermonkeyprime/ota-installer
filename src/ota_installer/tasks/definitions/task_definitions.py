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
    """Handles the definitions of various task categories."""

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def preparation(self) -> "PreparationTaskDefinitions":
        """Returns the preparation task definitions."""
        return PreparationTaskDefinitions()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Migration Tasks", char=" "
    )
    def migration(self) -> "MigrationTaskDefinitions":
        """Returns the migration task definitions."""
        return MigrationTaskDefinitions()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Application Tasks", char=" "
    )
    def application(self) -> "ApplicationTaskDefinitions":
        """Returns the application task definitions."""
        return ApplicationTaskDefinitions()


@dataclass
class TaskDefinitionsTemplate(object):
    """Template for task definitions."""

    tasks: StrTuple = field(default_factory=tuple)

    def __iter__(self) -> StrIterator:
        """Iterates over the task names."""
        return iter(self.tasks)


def enum_task_names(enum: Iterable) -> list:
    """Extracts task names from an enumeration."""
    result = [enum_member.value.value for enum_member in enum]
    logger.debug(f"enum_task_names(): {result=}")
    return result


@dataclass
class PreparationTaskDefinitions(TaskDefinitionsTemplate):
    """Defines preparation tasks."""

    def __post_init__(self) -> None:
        """Initializes the preparation tasks."""
        self.tasks = tuple(enum_task_names(PreparationTasks))


@dataclass
class MigrationTaskDefinitions(TaskDefinitionsTemplate):
    """Defines migration tasks."""

    def __post_init__(self) -> None:
        """Initializes the migration tasks."""
        self.tasks = tuple(enum_task_names(MigrationTask))


@dataclass
class ApplicationTaskDefinitions(TaskDefinitionsTemplate):
    """Defines application tasks."""

    def __post_init__(self) -> None:
        """Initializes the application tasks."""
        self.tasks = tuple(enum_task_names(ApplicationTasks))


# Signed off by Brian Sanford on 20260202
