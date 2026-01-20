# src/ota_installer/command_line_interface.py
from pathlib import Path

import typer

from . import application
from .log_setup import show_debug
from .program_versioning.software_version import (
    get_text_display,
)
from .tasks.execution.cli_arguments import CLIArguments
from .tasks.execution.task_execution import TaskGroupNames

cli = typer.Typer(help="Manually Install Android Device OTA Firmware")


def version_callback(value: bool) -> None:
    """Display version information and exit."""
    if value:
        typer.echo(get_text_display())  # Customize as needed
        raise typer.Exit()


def debug_callback(value: bool) -> None:
    """Enable debug logging if the flag is set."""
    if value:
        show_debug()


@cli.command()
def ota_installerer(
    path: str = typer.Argument(..., help="The path to the OTA file."),
    task_group: TaskGroupNames | None = typer.Option(
        None,
        "--task_group",
        "-t",
        help="Runs only the specified task group.",
        case_sensitive=False,
        show_choices=True,
        metavar="TASK",
    ),
    list_paths: bool = typer.Option(
        False,
        "--list",
        "-l",
        help="Lists paths and generated files.",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Lists version information.",
        callback=version_callback,
        is_eager=True,
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Displays debug loggers",
        callback=debug_callback,
        is_eager=True,
    ),
):
    """Install OTA firmware on an Android device.

    Args:
        path: The path to the OTA file.
        task_group: Optional task group to run.
        list_paths: Flag to list paths and generated files.
        version: Flag to display version information.
        debug: Flag to enable debug logging.
    """
    args = CLIArguments(
        path=Path(path),
        task_group=task_group.value if task_group else None,
        list=list_paths,
    )

    application.run()
    application.task_execution(args)


if __name__ == "__main__":
    cli()
# Signed off by Brian Sanford on 20260119
