# src/ota_installer/tasks/factories/task_factory.py
from collections.abc import Callable
from dataclasses import dataclass, field

from loguru import logger

from ...variables import VariableManager
from ..mappings import TASK_CLASS_MAP, TaskName


@dataclass
class TaskFactory(object):
    variable_manager: VariableManager | None = field(default=None)

    def factory_rules(self, task_name: str) -> type | None:
        try:
            # Normalize to UPPER_CASE to match Enum member names
            normalized_name = task_name.upper()
            task_enum = TaskName[normalized_name]
            return TASK_CLASS_MAP.get(task_enum)
        except KeyError as err:
            logger.error(f"No TaskName enum found for: {task_name!r}")
            return None
        except Exception as err:
            logger.exception(
                f"Unexpected error while resolving task {task_name!r}: {err}"
            )
            return None

    def create_task(self, task_name: str) -> Callable | None:
        task = self.factory_rules(task_name)
        if isinstance(task, type):
            return task(self.variable_manager)
