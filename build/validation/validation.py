#!/usr/bin/env python3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, StringConstraints, ValidationError

from build.components.file.structures import FileNameParserStructure


class VersionModel(BaseModel):
    version_string: Annotated[
        str,
        StringConstraints(pattern="^[a-z]{2}[1-9][a-z].[0-9]{6}.[0-9]{3}$"),
    ]


@dataclass
class Version(object):
    file_string: str
    file_name: str = field(init=False)
    file_name_parser: FileNameParserStructure = field(init=False)
    populate_model: VersionModel = field(init=False)

    def __post_init__(self) -> None:
        self.file_name = Path(self.file_string).stem
        self.file_name_parser = FileNameParserStructure(
            raw_name=str(self.file_name)
        )
        self.populate_model = VersionModel(
            version_string=self.file_name_parser.version,
        )

    def validation(self) -> None:
        try:
            self.populate_model
            print(f"{self.populate_model.version_string}")
        except ValidationError as error:
            error_items = str(error).strip().split("\n")
            error_message = error_items[2].strip()  # .split(" ")
            print(f"ValidationError: {error_message}")


def main() -> None:
    version = Version("tokay-ota-ap4a.250205.002-22cfd265.zip")
    version.validation()


if __name__ == "__main__":
    main()
