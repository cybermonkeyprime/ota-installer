from dataclasses import dataclass, field


@dataclass
class PatchedImageManager:
    image_name: str = field(default="place_holder")
