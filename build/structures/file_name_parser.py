from dataclasses import dataclass, field
from pathlib import Path
from pydantic import BaseModel, StringConstraints, ValidationError
from typing import Annotated, Any


@dataclass
class FileNameParser(object):
    raw_name: str
    parts: list[str] = field(init=False)
    device: str = field(init=False)
    file_type: str = field(init=False)
    version: str = field(init=False)
    extra: str | None = field(init=False)

    def __post_init__(self) -> None:
        self.parse_file_name()

    def parse_file_name(self) -> None:
        self.parts = self.raw_name.split("-")
        try:
            self.device, self.file_type, self.version, *extra_parts = self.parts
            self.extra = "-".join(extra_parts) if extra_parts else None
        except ValueError as e:
            raise ValueError(f"Error parsing file name: {self.raw_name}") from e

    def __str__(self) -> str:
        return self.raw_name


class VersionModel(BaseModel):
    version_string: Annotated[
        str, StringConstraints(pattern="^[a-z]{2}[1-9][a-z].[0-9]{6}.[0-9]{3}$")
    ]


@dataclass
class DataValidation(object):
    validation_instance: type
    model_instance: Any

    def validator(self):
        try:
            self.model_instance
        except ValidationError as error:
            error_items = str(error).strip().split("\n")
            error_message = error_items[2].strip()  # .split(" ")
            print(f"ValidationError- : {error_message}")


if __name__ == "__main__":
    file_string = "tokay-ota-ap4a.250205.00a-22cfd265.zip"
    file_name = Path(file_string).stem
    file_name_parser = FileNameParser(raw_name=str(file_name))
    version_model = VersionModel(
        version_string=file_name_parser.version,
    )
    print()
    data = DataValidation(VersionModel, version_model)
    data.validator()
