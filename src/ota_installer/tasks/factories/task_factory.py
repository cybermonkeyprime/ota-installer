# src/ota_installer/tasks/factories/task_factory.py
import uuid
from dataclasses import dataclass, field

from ...log_setup import logger
from ...variables.variable_manager import VariableManager
from ..plugin_registry import TASK_PLUGINS


@dataclass
class TaskFactory(object):
    variable_manager: VariableManager | None = field(default=None)
    run_id: str = field(
        default_factory=lambda: uuid.uuid4().hex[:8]
    )  # Unique ID per run

    def create_task(self, task_name: str):
        logger.debug(f"TaskFactory.create_task(): {task_name=}")
        task_class = TASK_PLUGINS.get(task_name)

        if not task_class:
            logger.bind(
                event="task_lookup", status="not_found", task=task_name
            ).error(f"No plugin task registered for: {task_name!r}")
            return None

        # Log structurally with bound context
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
