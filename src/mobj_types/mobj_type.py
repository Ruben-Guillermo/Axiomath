from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
from src.mobjs.mobj import Mobj

from src.puint import PositiveOrUndefinedInt, UndefinedEnum


if TYPE_CHECKING:
    from src.mobjs.custom_mobj import CustomMobj


@dataclass(frozen=True)
class MobjType(ABC):
    """A class that defines a custom mobj type"""

    name: str
    value_count: PositiveOrUndefinedInt

    @abstractmethod
    def __call__(self, *values: Mobj) -> CustomMobj:
        """Calling the MobjType returns an instance of the CustomMobj with that MobjType for syntactic sugar"""
        
        

