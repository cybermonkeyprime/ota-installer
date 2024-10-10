import argparse
from dataclasses import dataclass, field


@dataclass
class CommandLineInterface(object):
    task_group: str | None = field(default=None)
    list_paths: bool = field(default=False)
    ota_file_path: str = field(default="")

    def parse_arguments(self) -> argparse.Namespace:
        parser = self._create_argument_parser()
        args = self._try_parse_arguments(parser)
        self._update_fields_from_args(args)
        return args

    @staticmethod
    def _create_argument_parser() -> argparse.ArgumentParser:
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
        try:
            return parser.parse_args()
        except argparse.ArgumentError as e:
            print(f"Error parsing arguments: {e}")
            parser.print_help()
            raise

    def _update_fields_from_args(self, args: argparse.Namespace) -> None:
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
