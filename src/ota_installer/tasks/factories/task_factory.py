# src/ota_installer/tasks/factories/task_factory.py
from dataclasses import dataclass, field

from loguru import logger

from ...variables import VariableManager
from ..plugin_registry import TASK_PLUGINS


@dataclass
class TaskFactory(object):
    variable_manager: VariableManager | None = field(default=None)

    def create_task(self, task_name: str):
        logger.debug(f"TaskFactory.create_task(): {task_name=}")
        task_class = TASK_PLUGINS.get(task_name)
        if not task_class:
            logger.error(f"No plugin task registered for: {task_name!r}")
            return None
        return task_class(self.variable_manager)
