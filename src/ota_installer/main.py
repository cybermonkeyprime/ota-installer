#!/usr/bin/env python3

from .command_line_interface import cli
from .tasks import plugin_loader


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
