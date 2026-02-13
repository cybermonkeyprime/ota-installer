# src/ota_installer/types/decorators.py
from collections.abc import Callable
from typing import Protocol, TypeVar

R = TypeVar("R")

"""
Shared Protocols for decorator typing.

- GenericDecorator[R]: for decorators that preserve the return type.
- StringReturningDecorator: for decorators that transform or always return str.

These are intended to be used with class-based decorators implementing
__call__.
"""


class GenericDecorator(Protocol[R]):
    def __call__(self, func: Callable[..., R]) -> Callable[..., R]: ...


class StringReturningDecorator(Protocol):
    def __call__(self, func: Callable[..., str]) -> Callable[..., str]: ...


# Signed off by Brian Sanford on 20260213
