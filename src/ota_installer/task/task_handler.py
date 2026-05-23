# tasks/task_handler.py
from dataclasses import dataclass
from functools import partial

from .. import decorator
from .task_group_handler import (
    ApplicationTask,
    MigrationTask,
    PreparationTask,
)

task_prompt: partial = partial(decorator.ConfirmationPrompt, char=" ")


@dataclass
class TaskDefinitions:
    """Handles the definitions of various task categories."""

    @decorator.PaddedFooterWrapper()
    @task_prompt(comment="perform the Preparation Tasks")
    def preparation(self) -> tuple:
        """Returns the preparation task definitions."""
        return PreparationTask.get_member_names()

    @decorator.PaddedFooterWrapper()
    @task_prompt(comment="perform the Migration Tasks")
    def migration(self) -> tuple:
        """Returns the migration task definitions."""
        return MigrationTask.get_member_names()

    @decorator.PaddedFooterWrapper()
    @task_prompt(comment="perform the Application Tasks")
    def application(self) -> tuple:
        """Returns the application task definitions."""
        return ApplicationTask.get_member_names()


# Signed off by Brian Sanford on 20260509
