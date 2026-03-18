from .command_line_interface import cli

# DO NOT REMOVE, PLUGIN LOADERS!!!
from .dispatchers import dispatcher_plugin_loader
from .tasks import plugin_loader


def main() -> None:
    """Entry point for the application.

    Initializes the command line interface.
    """
    cli()


if __name__ == "__main__":
    main()
