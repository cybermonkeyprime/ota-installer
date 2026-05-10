from .command_line_interface import cli

# DO NOT REMOVE, PLUGIN LOADERS!!!
from .dispatchers.plugins import dispatcher_plugin_loader
from .tasks.plugins import task_plugin_loader


def main() -> None:
    """Entry point for the application.

    Initializes the command line interface.
    """
    cli()


if __name__ == "__main__":
    main()
