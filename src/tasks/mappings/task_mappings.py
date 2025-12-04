# src/tasks/mappings/task_mappings.py
from collections.abc import Iterable

from .bindings import TASK_CLASS_MAP
from .constants import TaskName
from .definitions import TaskDefinitions


def execute_all_tasks(tasks: Iterable[TaskName]) -> None:
    for task_name in tasks:
        task_class = TASK_CLASS_MAP[task_name]
        instance = task_class()
        instance.run()


def print_task_actions() -> None:
    definitions = TaskDefinitions().map()
    for group, task_list in definitions.items():
        print(f"Group: {group}")
    for task in task_list:
        print(f" - {task.name}")
