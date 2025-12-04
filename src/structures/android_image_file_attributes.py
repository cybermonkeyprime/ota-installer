from dataclasses import dataclass, field


@dataclass
class AndroidImageFileAttributes:
    name: str = field(default="")
    extension: str = field(default="")
