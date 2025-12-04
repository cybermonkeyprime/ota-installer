from dataclasses import dataclass, field


@dataclass
class ImageFileAttributeStructure:
    name: str = field(default="")


@dataclass
class ImageFileStructure:
    attributes: ImageFileAttributeStructure = field(
        default_factory=ImageFileAttributeStructure
    )

    def __init__(self, item: list[str]) -> None:
        try:
            self.attributes = ImageFileAttributeStructure(*item)
        except TypeError as e:
            raise ValueError("Invalid item list provided to AndroidImageFile") from e
