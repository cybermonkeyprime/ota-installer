# src/ota_installer/tasks/factories/task_factory.py
import uuid
from dataclasses import dataclass, field

from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from ..plugin_registry import TASK_PLUGINS


@dataclass
class TaskFactory(object):
    """Factory for creating task instances.

    Attributes:
        variable_manager: An instance of VariableManager or None.
        run_id: A unique identifier for the task run.
    """

    variable_manager: VariableManager | None = field(default=None)
    run_id: str = field(
        default_factory=lambda: uuid.uuid4().hex[:8]
    )  # Unique ID per run

    def create_task(self, task_name: str) -> object | None:
        """Creates a task instance based on the provided task name."""
        logger.debug(f"Creating task: {task_name=}")
        task_class = TASK_PLUGINS.get(task_name)

        if not task_class:
            self._log_task_not_found(task_name)
            return None

        return self._initialize_task(task_class, task_name)

    def _log_task_not_found(self, task_name: str) -> None:
        """logs an error when a task is not found."""
        logger.bind(
            event="task_lookup", status="not_found", task=task_name
        ).error(f"no plugin task registered for: {task_name!r}")

    def _initialize_task(self, task_class: type, task_name: str) -> object:
        """Initializes a task instance with logging."""
        task_logger = logger.bind(
            event="task_init",
            task=task_name,
            plugin=task_class.__name__,
            run_id=self.run_id,
        )
        task_logger.info("Creating task instance")

        task_instance = task_class(self.variable_manager)
        task_instance.logger = task_logger
        return task_instance


# Signed off by Brian Sanford on 20260203
