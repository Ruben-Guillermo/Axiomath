# Unit tests for custom_mobj.py

import pytest
from src.mobj_types.dynamic_or_uint import DynamicOrUint
from src.mobj_types.mobj_type import MobjType
from src.mobj_types.value_structure import ValueStructure
from src.mobjs.custom_mobj import CustomMobj
from src.mobjs.variable import Variable



def test_custom_mobj_default():
    type = MobjType("TestType", ValueStructure.non_defining(2))
    mobj = CustomMobj(type, Variable("a"), Variable("b"))

    assert mobj.type == type
    assert mobj.values == (Variable("a"), Variable("b"))
    assert mobj.variables == {"a", "b"}
    assert mobj.defined_variables == set()

    assert mobj == type(Variable("a"), Variable("b"))

    type2 = MobjType("TestType2", ValueStructure.defines_first(2))
    mobj2 = CustomMobj(type2, Variable("a"), Variable("b"))

    assert mobj2.type == type2
    assert mobj2.values == (Variable("a"), Variable("b"))
    assert mobj2.variables == {"a", "b"}
    assert mobj2.defined_variables == {"a"}

    assert mobj2 == type2(Variable("a"), Variable("b"))

    type3 = MobjType("TestType3", ValueStructure.dynamic())

    mobj3a = CustomMobj(type3, Variable("a"), Variable("b"))
    mobj3b = CustomMobj(type3, Variable("a"), Variable("b"), Variable("c"))

    assert mobj3a.type == type3
    assert mobj3a.values == (Variable("a"), Variable("b"))
    assert mobj3a.variables == {"a", "b"}
    assert mobj3a.defined_variables == set()
    assert mobj3a == type3(Variable("a"), Variable("b"))

    assert mobj3b.type == type3
    assert mobj3b.values == (Variable("a"), Variable("b"), Variable("c"))
    assert mobj3b.variables == {"a", "b", "c"}
    assert mobj3b.defined_variables == set()
    assert mobj3b == type3(Variable("a"), Variable("b"), Variable("c"))

    type4 = MobjType("TestType4", ValueStructure.non_defining(0))
    mobj4 = CustomMobj(type4)

    assert mobj4.type == type4
    assert mobj4.values == ()
    assert mobj4.variables == set()
    assert mobj4.defined_variables == set()
    assert mobj4 == type4()


def test_custom_mobj_invalid_value_count():
    type = MobjType("TestType", ValueStructure.non_defining(2))

    with pytest.raises(ValueError):
        CustomMobj(type, Variable("a"))

    with pytest.raises(ValueError):
        CustomMobj(type, Variable("a"), Variable("b"), Variable("c"))

    type2 = MobjType("TestType2", ValueStructure.defines_first(2))

    with pytest.raises(ValueError):
        CustomMobj(type2, Variable("a"))

    with pytest.raises(ValueError):
        CustomMobj(type2, Variable("a"), Variable("b"), Variable("c"))

    type3 = MobjType("TestType3", ValueStructure.dynamic())

    with pytest.raises(ValueError):
        CustomMobj(type3)

    type4 = MobjType("TestType4", ValueStructure.non_defining(0))

    with pytest.raises(ValueError):
        CustomMobj(type4, Variable("a"))

    with pytest.raises(ValueError):
        CustomMobj(type4, Variable("a"), Variable("b"))


def test_custom_mobj_invalid_variable_defining_spots():
    type1 = MobjType("TestType1", ValueStructure.non_defining(0))
    type2 = MobjType("TestType2", ValueStructure.defines_first(1))
    a = type1()
    with pytest.raises(ValueError):
        type2(a)


def test_custom_mobj_invalid_use_of_defined_variable():
    type1 = MobjType("TestType1", ValueStructure.defines_first(1))
    type2 = MobjType("TestType2", ValueStructure.non_defining(1))
    type3 = MobjType("TestType3", ValueStructure.non_defining(2))

    a = type1(Variable("a"))
    b = type2(Variable("a"))
    with pytest.raises(ValueError):
        type3(a, b)


def test_custom_mobj_recursive_definition():
    type1 = MobjType("TestType1", ValueStructure.defines_first(2))

    a = type1(Variable("a"), Variable("b"))
    with pytest.raises(ValueError):
        type1(Variable("a"), a)
