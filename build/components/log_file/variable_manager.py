from dataclasses import dataclass, field
from typing import Any

from build.components.file.structures import FileNameParserStructure


@dataclass
class LogFileManager(object):
    """
    Generates a log file name based on the file name parser.

    Attributes:
        file_name_parser: An instance of FileNameParser used to parse device
        and version information for the log file name.
    """

    parser: Any = field(default_factory=lambda: FileNameParserStructure)

    def __str__(self) -> str:
        """
        Generates a log file path string.

        Returns:
            A string representing the log file path.
        """

        return f"/tmp/ota_variables_{self.parser.device}_{self.parser.version}.txt"


def main():
    # Example usage
    log_file_manager = LogFileManager(("device", "version"))
    print(str(log_file_manager))


if __name__ == "__main__":
    main()
