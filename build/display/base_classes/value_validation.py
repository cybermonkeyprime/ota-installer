from dataclasses import dataclass, field

from dispatchers import DispatcherManager

from build.dispatchers.dispatcher_template import (
    CollectionDictionary,
    DispatcherTemplate,
)


@dataclass
class ValueValidation(object):
    """Validates values using a dispatch handler."""

    dispatch_handler: DispatcherManager = field(default_factory=DispatcherManager)

    def fetcher(self) -> DispatcherTemplate:
        return self.dispatch_handler.get_dispatcher()

    def validate_value(self, key: str) -> CollectionDictionary:
        value = self.fetcher().get_value(key=key)
        value = self.dispatch_handler.get_dispatcher().get_value(key=key)
        if value is None:
            print(f"{value=}")
        return value
