# src/ota_installer/tasks/definitions/task_definitions.py
from dataclasses import dataclass
from functools import partial

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

task_prompt = partial(decorators.ConfirmationPrompt, char=" ")


@dataclass
class TaskDefinitions(object):
    """Handles the definitions of various task categories."""

    @decorators.PaddedFooterWrapper()
    @task_prompt(comment="perform the Preparation Tasks")
    def preparation(self) -> tuple:
        """Returns the preparation task definitions."""
        return PreparationTask.get_member_names()

    @decorators.PaddedFooterWrapper()
    @task_prompt(comment="perform the Migration Tasks")
    def migration(self) -> tuple:
        """Returns the migration task definitions."""
        return MigrationTask.get_member_names()

    @decorators.PaddedFooterWrapper()
    @task_prompt(comment="perform the Application Tasks")
    def application(self) -> tuple:
        """Returns the application task definitions."""
        return ApplicationTask.get_member_names()


