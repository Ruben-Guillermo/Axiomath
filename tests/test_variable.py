# Unit tests for variable.py

import pytest
from src.mobj_types.value_structure import ValueStructure
from src.mobjs.variable import Variable, VariableType


def test_variable_default():
    a = Variable("a")
    assert a.var_name == "a"
    assert a.type == VariableType
    assert a.variables == {"a"}
    assert a.defined_variables == set()
    assert a.values == tuple()
    
    a_type  = a.type
    assert a_type.name == "Variable"
    assert a_type.structure == ValueStructure.non_defining(0)
    

def test_variable_invalid():
    with pytest.raises(ValueError):
        Variable("")
        
def test_variable_evaluate():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    
    assert a.evaluate({}) == a
    assert b.evaluate({}) == b
    assert c.evaluate({}) == c
    
    assert a.evaluate({"a": b}) == b
    assert b.evaluate({"a": b}) == b
    assert c.evaluate({"a": b}) == c
    
    assert a.evaluate({"a": b, "b": c}) == b
    assert b.evaluate({"a": b, "b": c}) == c
    assert c.evaluate({"a": b, "b": c}) == c

def test_get_sub_mobj():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    
    assert a.get_sub_mobj() == a
    assert b.get_sub_mobj() == b
    assert c.get_sub_mobj() == c
    
    with pytest.raises(IndexError):
        a.get_sub_mobj(0)
    with pytest.raises(IndexError):
        b.get_sub_mobj(1)
    with pytest.raises(IndexError):
        c.get_sub_mobj(0, 0)

def test_create_dictionary_from():
    a = Variable("a")
    b = Variable("b")
    c = Variable("c")
    
    assert a.create_dictionary_from(a) == {"a": a}
    assert b.create_dictionary_from(a) == {"b": a}
    assert c.create_dictionary_from(a) == {"c": a}

def test_eq():
    a = Variable("a")
    b = Variable("b")
    a2 = Variable("a")
    
    assert a == a2
    assert a != b
    assert a != 1
