from dataclasses import dataclass, field

from pydantic import BaseModel, FilePath


@dataclass
class FileExistenceModel(BaseModel):
    """Checks the existence of a file."""

    file_path: FilePath = field(init=False)

    def checker(self):
        try:
            self.file_path.exists()
        except FileNotFoundError:
            print(f"Warning, {self.file_path} doesn't exist.")
        finally:
            return self.file_path
