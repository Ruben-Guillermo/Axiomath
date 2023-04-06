# Unit tests for the puint module

from src.puint import PositiveOrUndefinedInt, UndefinedEnum
import pytest


def test_puint_default():
    puint1 = PositiveOrUndefinedInt(UndefinedEnum.UNDEFINED)
    assert puint1.value == UndefinedEnum.UNDEFINED
    assert not puint1.defined

    puint2 = PositiveOrUndefinedInt(1)
    assert puint2.value == 1
    assert puint2.defined


def test_puint_error():
    with pytest.raises(ValueError):
        PositiveOrUndefinedInt(-1)
    with pytest.raises(ValueError):
        PositiveOrUndefinedInt(0)
    with pytest.raises(ValueError):
        PositiveOrUndefinedInt(1.5)
