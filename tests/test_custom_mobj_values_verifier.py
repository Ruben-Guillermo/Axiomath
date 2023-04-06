# Unit tests for custom_mobj_values_verifier.py

import pytest
from src.mobj_types.dynamic_or_uint import DynamicOrUint
from src.mobjs.custom_mobj_values_verifier import check_number_of_values_is_correct


def test_number_of_values_is_correct():
    check_number_of_values_is_correct(DynamicOrUint(2), 2)
    check_number_of_values_is_correct(DynamicOrUint(0), 0)
    check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 1)
    check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 50)


def test_numbers_of_values_is_correct_invalid():
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint(2), 1)
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint(2), 3)
    with pytest.raises(ValueError):
        check_number_of_values_is_correct(DynamicOrUint.greater_than_0(), 0)
