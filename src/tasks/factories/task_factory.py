from collections.abc import Callable
from dataclasses import dataclass, field

from loguru import logger

import src.tasks.mappings as task_mappings
import src.variables as variables


@dataclass
class TaskFactory(object):
    variable_manager: variables.VariableManager | None = field(default=None)

    def factory_rules(self, task_name: str) -> type | None:
        try:
            # Normalize to UPPER_CASE to match Enum member names
            normalized_name = task_name.upper()
            task_enum = task_mappings.TaskName[normalized_name]
            return task_mappings.TASK_CLASS_MAP.get(task_enum)
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
