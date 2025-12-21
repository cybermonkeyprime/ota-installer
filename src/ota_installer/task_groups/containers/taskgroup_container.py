# src/ota_installer/task_groups/containers/taskgroup_container.py
from collections import namedtuple

TaskGroupContainer = namedtuple(
    "TaskGroupContainer", ["group_name", "group_enum"]
)
