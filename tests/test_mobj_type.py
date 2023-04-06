# Unit tests for mobj_type.py

from src.mobj_types.mobj_type import MobjType
from src.mobj_types.value_structure import ValueStructure


def test_mobj_type_default():
    a = MobjType("a", ValueStructure.dynamic())
    b = MobjType("b", ValueStructure.non_defining(1))
    c = MobjType("c", ValueStructure.defines_first(2))

    assert a.name == "a"
    assert b.name == "b"
    assert c.name == "c"

    assert a.structure == ValueStructure.dynamic()
    assert b.structure == ValueStructure.non_defining(1)
    assert c.structure == ValueStructure.defines_first(2)
    
