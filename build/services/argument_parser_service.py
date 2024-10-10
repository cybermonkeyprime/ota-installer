from argparse import Namespace
from dataclasses import dataclass, field

from build.command_line_interface import CommandLineInterface


@dataclass
class ArgumentParserService(object):
    cli_interface: CommandLineInterface = field(default_factory=CommandLineInterface)

    def parse_cli_arguments(self) -> Namespace:
        try:
            return self.cli_interface.parse_arguments()
        except Exception as error:
            raise RuntimeError("Failed to parse command line arguments") from error


def run_argument_parser() -> None:
    argument_parser_service = ArgumentParserService()
    try:
        parsed_arguments: Namespace = argument_parser_service.parse_cli_arguments()
        # Assuming there's a function to handle the parsed arguments
        # handle_parsed_arguments(parsed_arguments)
    except RuntimeError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run_argument_parser()
