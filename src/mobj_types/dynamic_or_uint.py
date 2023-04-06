from __future__ import annotations

from enum import Enum, auto
from typing import Union


class Dynamic(Enum):
    GREATER_THAN_0 = auto()


class DynamicOrUint:
    """A class that represents a positive integer or undefined. x >= 0 or undefined"""

    def __init__(self, value: Union[int, Dynamic]):
        self.value = value
        if isinstance(value, int):
            if value < 0:
                raise ValueError(
                    f"Value must be positive or undefined. Provided {value}"
                )
        elif value != Dynamic.GREATER_THAN_0:
            raise ValueError(f"Value must be positive or undefined. Provided {value}")

    @property
    def is_int(self) -> bool:
        return isinstance(self.value, int)

    def __eq__(self, other: DynamicOrUint) -> bool:
        return self.value == other.value

    @staticmethod
    def greater_than_0() -> DynamicOrUint:
        return DynamicOrUint(Dynamic.GREATER_THAN_0)
