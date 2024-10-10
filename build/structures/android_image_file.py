from dataclasses import dataclass
from typing import List

from .android_image_file_attributes import AndroidImageFileAttributes


@dataclass
class AndroidImageFile:
    attributes: AndroidImageFileAttributes

    def __init__(self, item: List[str]) -> None:
        try:
            self.attributes = AndroidImageFileAttributes(*item)
        except TypeError as e:
            raise ValueError("Invalid item list provided to AndroidImageFile") from e
