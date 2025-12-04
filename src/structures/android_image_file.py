from dataclasses import dataclass

from .android_image_file_attributes import AndroidImageFileAttributes


@dataclass(init=False)
class AndroidImageFile(object):
    attributes: AndroidImageFileAttributes

    def __init__(self, item: list[str]) -> None:
        self.set_attributes(item)

    def set_attributes(self, item: list[str]) -> None:
        try:
            self.attributes = AndroidImageFileAttributes(*item)
        except TypeError as err:
            raise ValueError(
                "Invalid item list provided to AndroidImageFile"
            ) from err
