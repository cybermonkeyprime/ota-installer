from dataclasses import dataclass, field

from build.dispatchers.dispatcher_template import DispatcherTemplate


@dataclass
class DefaultImageType(object):
    def __str__(self) -> str:
        return "init_boot"


@dataclass
class ImageTypeDispatcher(DispatcherTemplate):
    obj: str = field(default_factory=lambda: "")

    @property
    def collection(self):
        return {}

    def get_key(self, key: str) -> type | DefaultImageType | str:
        return self.collection.get(key, DefaultImageType())
