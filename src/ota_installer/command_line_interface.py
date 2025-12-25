# src/ota_installer/command_line_interface.py
import sys
from pathlib import Path

import typer

from .application import Application, task_execution
from .log_setup import logger
from .program_versioning import SoftwareVersion
from .tasks.execution.cli_arguments import CLIArguments
from .tasks.execution.task_execution import TaskGroupNames

cli = typer.Typer(help="Manually Install Android Device OTA Firmware")


def version_callback(value: bool) -> None:
    if value:
        typer.echo(SoftwareVersion().display)  # Customize as needed
        raise typer.Exit()


def debug_callback(value: bool) -> None:
    if value:
        logger.remove()  # remove default handler
        logger.add(sys.stderr, level="DEBUG")


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
    args = CLIArguments(
        path=Path(path),
        task_group=task_group.value if task_group else None,
        list=list_paths,
    )

    app_instance = Application()
    app_instance.run()

    task_execution(args)


if __name__ == "__main__":
    # main()
    cli()
