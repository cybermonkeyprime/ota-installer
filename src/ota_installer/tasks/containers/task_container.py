# src/ota_installer/tasks/containers/task_container.py
from collections import namedtuple

TaskContainer = namedtuple("TaskContainer", ["task_name", "task_class"])
