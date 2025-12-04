# src/tasks/components/base_task.py
from dataclasses import dataclass

from src.tasks.task_operation_processor import TaskOperationProcessor


@dataclass
class BaseTask(object):
    def __init__(
        self, enum_values, command_string=None, comment=None, reminder=None
    ):
        self.task = TaskOperationProcessor()
        self.task.set_item("index", enum_values.INDEX.value)
        self.task.set_item("title", enum_values.TITLE.value)
        self.task.set_item("description", enum_values.DESCRIPTION.value)

        if command_string:
            self.task.set_item("command_string", command_string)
        if comment:
            self.task.set_item("comment", comment)
        if reminder:
            self.task.set_item("reminder", reminder)
