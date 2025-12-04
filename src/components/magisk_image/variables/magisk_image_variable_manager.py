from dataclasses import dataclass, field


@dataclass
class MagiskImageVariableManager:
    """
    Manages the details of an image.

    Attributes:
        image_name (str): The name of the image. Defaults to "placeholder".
    """

    image_name: str = field(default="place_holder")
