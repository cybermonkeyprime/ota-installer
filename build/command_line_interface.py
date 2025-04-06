import argparse
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CommandLineInterface(object):
    """Command Line Interface for OTA Firmware Installation.

    Attributes:
        task_group: An optional string specifying the task group to run.
        list_paths: A boolean indicating whether to list paths and generated files.
        ota_file_path: The path to the OTA file.
    """
    task_group: Optional[str] = field(default=None)
    list_paths: bool = field(default=False)
    ota_file_path: str = field(default="")

    def parse_arguments(self) -> argparse.Namespace:
        """Parses command line arguments and updates the instance fields."""
        parser = self._create_argument_parser()
        args = self._try_parse_arguments(parser)
        self._update_fields_from_args(args)
        return args

    @staticmethod
    def _create_argument_parser() -> argparse.ArgumentParser:
        """Creates and configures the argument parser."""
        parser = argparse.ArgumentParser(
            prog="ota-installer",
            description="Manually Install Android Device OTA Firmware",
            epilog="Thanks for using %(prog)s!",
        )
        parser.add_argument(
            "-t",
            "--task_group",
            choices=("preparation", "migration", "application"),
            help="Runs only the specified task group.",
        )
        parser.add_argument(
            "-l", "--list", action="store_true", help="Lists paths and generated files."
        )
        parser.add_argument(
            "-v", "--version", action="store_true", help="Lists version information."
        )
        parser.add_argument("path", type=str, help="The path to the OTA file.")
        return parser

    def _try_parse_arguments(
        self, parser: argparse.ArgumentParser
    ) -> argparse.Namespace:
        """Attempts to parse the arguments, handling any errors."""
        try:
            return parser.parse_args()
        except argparse.ArgumentError as e:
            print(f"Error parsing arguments: {e}")
            parser.print_help()
            raise

    def _update_fields_from_args(self, args: argparse.Namespace) -> None:
        """Updates the dataclass fields with the parsed arguments."""
        self.task_group = args.task_group
        self.list_paths = args.list
        self.ota_file_path = args.path


def main() -> None:
    cli = CommandLineInterface()
    parsed_args = cli.parse_arguments()
    # Now you can use parsed_args or the fields of cli
    # Example: print(cli.ota_file_path)


if __name__ == "__main__":
    main()
