from dataclasses import dataclass

from src.mobj_types.value_structure import ValueStructure
from src.mobjs.mobj import Mobj


@dataclass
class MobjType:
    """Represents a type of mobj, like Implication, Union, etc."""

    name: str
    _structure: ValueStructure

    @property
    def structure(self) -> ValueStructure:
        """The number of values that the MobjType takes"""
        return self._structure

    def __call__(self, *values: Mobj) -> Mobj:
        """Calling the MobjType returns an instance of the CustomMobj with that MobjType for syntactic sugar"""
        from src.mobjs.custom_mobj import CustomMobj

        return CustomMobj(self, *values)


