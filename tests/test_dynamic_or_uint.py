# Unit tests for dynamic_or_uint.py

import pytest
from src.mobj_types.dynamic_or_uint import Dynamic, DynamicOrUint


def test_dynamic_or_uint_default():
    a = DynamicOrUint(1)
    b = DynamicOrUint(Dynamic.GREATER_THAN_0)

    assert a.is_int
    assert not b.is_int

    assert a.value == 1
    assert b.value == Dynamic.GREATER_THAN_0

    c = DynamicOrUint(0)

    assert c.is_int
    assert c.value == 0


def test_dynamic_or_uint_invalid():
    with pytest.raises(ValueError):
        DynamicOrUint(-1)
    with pytest.raises(ValueError):
        DynamicOrUint(1.1)

def test_greater_than_0():
    a = DynamicOrUint.greater_than_0()
    assert not a.is_int
    assert a.value == Dynamic.GREATER_THAN_0
    assert a == DynamicOrUint(Dynamic.GREATER_THAN_0)