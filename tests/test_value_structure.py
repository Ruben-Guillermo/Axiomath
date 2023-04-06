# Unit tests for value_structure.py

import pytest
from src.mobj_types.dynamic_or_uint import Dynamic, DynamicOrUint
from src.mobj_types.value_structure import ValueStructure


def test_value_structure_default():
    a = ValueStructure(DynamicOrUint(1), [False])
    b = ValueStructure(DynamicOrUint.greater_than_0(), None)
    c = ValueStructure(DynamicOrUint(1), [True])

    assert not a.does_define
    assert not b.does_define
    assert c.does_define

    assert not a.is_spot_variable_defining(0)
    assert not b.is_spot_variable_defining(0)
    assert c.is_spot_variable_defining(0)

    assert a.value_count.value == 1
    assert b.value_count.value == Dynamic.GREATER_THAN_0
    assert c.value_count.value == 1
    
def test_value_structure_invalid():
    with pytest.raises(ValueError):
        ValueStructure(DynamicOrUint(1), None)
    with pytest.raises(ValueError):
        ValueStructure(DynamicOrUint(1), [True, False])
    with pytest.raises(ValueError):
        ValueStructure(DynamicOrUint.greater_than_0(), [True, False])
    
def test_value_structure_static():
    a = ValueStructure.dynamic()
    b = ValueStructure.non_defining(1)
    c = ValueStructure.defines_first(2)

    assert not a.does_define
    assert not b.does_define
    assert c.does_define

    assert not a.is_spot_variable_defining(0)
    assert not b.is_spot_variable_defining(0)
    assert c.is_spot_variable_defining(0)
    assert not c.is_spot_variable_defining(1)

    assert a.value_count.value == Dynamic.GREATER_THAN_0
    assert b.value_count.value == 1
    assert c.value_count.value == 2


def test_value_structure_eq():
    a = ValueStructure(DynamicOrUint(1), [False])
    b = ValueStructure(DynamicOrUint.greater_than_0(), None)
    c = ValueStructure(DynamicOrUint(1), [True])

    assert a == a
    assert b == b
    assert c == c

    assert a != b
    assert a != c
    assert b != c

    assert b == ValueStructure(DynamicOrUint.greater_than_0(), None)
