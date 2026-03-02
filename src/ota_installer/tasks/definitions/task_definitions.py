# src/ota_installer/tasks/definitions/task_definitions.py
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field

from loguru import logger

from ... import decorators
from ...task_groups.constants.application_task import (
    ApplicationTask,
)
from ...task_groups.constants.migration_task import (
    MigrationTask,
)
from ...task_groups.constants.preparation_task import (
    PreparationTask,
)


@dataclass
class TaskDefinitions(object):
    """Handles the definitions of various task categories."""

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Preparation Tasks",
        char=" ",
    )
    def preparation(self) -> tuple:
        """Returns the preparation task definitions."""
        return PreparationTask.get_member_names()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Migration Tasks", char=" "
    )
    def migration(self) -> tuple:
        """Returns the migration task definitions."""
        return MigrationTask.get_member_names()

    @decorators.PaddedFooterWrapper()
    @decorators.ConfirmationPrompt(
        comment="perform the Application Tasks", char=" "
    )
    def application(self) -> tuple:
        """Returns the application task definitions."""
        return ApplicationTask.get_member_names()


# Signed off by Brian Sanford on 20260202
