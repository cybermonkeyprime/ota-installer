from .command_line_interface import cli

# DO NOT REMOVE, PLUGIN LOADERS!!!
from .plugin.loader import dispatcher_plugin_loader, task_plugin_loader


def main() -> None:
    """Entry point for the application.

    Initializes the command line interface.
    """
    cli()


if __name__ == "__main__":
    main()
# Signed off by Brian Sanford on 20260611
