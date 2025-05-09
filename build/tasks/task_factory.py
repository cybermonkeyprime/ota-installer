from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional

from build.tasks.factory_template import TaskFactoryTemplate
from build.tasks.task_mappings import TaskNameMapping
from build.variables import VariableManager


class TaskCreationError(Exception):
    """Custom exception for task creation errors."""


@dataclass
class AbstractTaskFactory(ABC):
    """Abstract base class for task factories."""

    @abstractmethod
    def create_task(self, task_name: str) -> Any:
        raise NotImplementedError()


@dataclass
class TaskFactory(AbstractTaskFactory):
    """Factory class to create task objects based on a given task name.

    Attributes:
        variable_manager: An instance of VariableManager to manage variables.
        task_mapping: A dictionary mapping task names to their respective
        classes.
    """

    variable_manager: Optional[VariableManager] = field(default=None)
    task_mapping: TaskNameMapping = field(default_factory=TaskNameMapping)

    def create_task(self, task_name: str) -> "type[TaskFactoryTemplate]":
        """Creates a task object based on the task name.

        Args:
            task_name: The name of the task to create.

        Returns:
            An instance of the task class associated with the task name.

        Raises:
            TaskCreationError: If the task name is not recognized.
        """
        try:
            task_class = self.task_mapping.task_map.get(
                task_name, InvalidKeyException(task_name)
            )
            return task_class(self.variable_manager)
        except KeyError as error:
            raise TaskCreationError(
                f"Task '{task_name}' is not recognized."
            ) from error


@dataclass
class InvalidKeyException(object):
    task_name: str = field(default_factory=str)

    def __str__(self) -> str:
        return f"Invalid Key: {self.task_name}"
