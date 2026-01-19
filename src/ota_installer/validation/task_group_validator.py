# validation/task_group_validator.py
from rich.console import console

from ..task_groups.constants.task_group_names import TaskGroupNames


def validate_task_group(value: str) -> TaskGroupNames:
    """Validate the provided task group name."""
    try:
        return TaskGroupNames[value.upper()]
    except KeyError:
        validate_task_groups = ", ".join(
            [task_group.name for task_group in TaskGroupNames]
        )
        console.print(
            f"[red]Error:[/red] Invalid task group '{value}'. "
            f"Valid options are: [cyan]{validate_task_groups}[/cyan]"
        )
        raise SystemExit(1) from None


# Signed off by Brian Sanford on 20260119
