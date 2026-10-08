# src/ota_installer/task/operation/image_path_resolver.py
from dataclasses import dataclass
from pathlib import Path

from ...plugin.plugin_dispatcher_adapter import PluginDispatcherAdapter
from ...plugin.plugin_type import PluginType


@dataclass(slots=True, frozen=True)
class ImagePathResolver:
    key: str

    @property
    def dispatcher(self) -> PluginDispatcherAdapter:
        return PluginDispatcherAdapter(PluginType.IMAGE)

    @property
    def retriever(self) -> object:
        return self.dispatcher.load()

    def resolve_path(self) -> Path:
        """Handles image retrieval based on a key."""
        return (
            Path.home() / "images" / f"{self.retriever.get_key(self.key)}.img"
        )


def resolve_image_path(key: str) -> Path:
    """Handles image retrieval based on a key."""
    return ImagePathResolver(key).resolve_path()


# Signed off by Brian Sanford on 20261007
