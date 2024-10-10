from dataclasses import dataclass, field


@dataclass
class ImageFile:
    file_name: str = field(default_factory=str)
    directory_path: str = field(default_factory=str)

    def get_full_path(self) -> str:
        try:
            if self.file_name and self.directory_path:
                return f"{self.directory_path}/{self.file_name}"
            raise ValueError("Both file_name and directory_path must be provided.")
        except ValueError as error:
            return str(error)

    def __str__(self) -> str:
        return self.get_full_path()
