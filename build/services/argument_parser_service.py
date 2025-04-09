from argparse import Namespace
from dataclasses import dataclass, field

from build.command_line_interface import CommandLineInterface


@dataclass
class ArgumentParserService(object):
    """Handles the parsing of command line arguments.

    Attributes:
        cli_interface: An instance of CommandLineInterface used to parse arguments.
    """
    cli_interface: CommandLineInterface = field(default_factory=CommandLineInterface)

    def parse_cli_arguments(self) -> Namespace:
        """Parses the command line arguments using the CLI interface.

        Returns:
            A Namespace object containing the parsed arguments.

        Raises:
            RuntimeError: If the parsing fails.
        """
        try:
            return self.cli_interface.parse_arguments()
        except Exception as error:
            raise RuntimeError("Failed to parse command line arguments") from error

def handle_parsed_arguments(arguments: Namespace) -> None:
    """Process the parsed arguments.

    Args:
        arguments: A Namespace object containing the parsed arguments.
    """
    # Placeholder for argument handling logic
    pass

def main(cli_interface: CommandLineInterface) -> None:
    """Main function to run the argument parser service.

    Args:
        cli_interface: An instance of CommandLineInterface for dependency injection.
    """
    argument_parser_service = ArgumentParserService(cli_interface)
    try:
        parsed_arguments = argument_parser_service.parse_cli_arguments()
        handle_parsed_arguments(parsed_arguments)
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main(CommandLineInterface())
