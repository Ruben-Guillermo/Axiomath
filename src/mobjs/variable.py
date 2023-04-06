from src.mobj_types.value_structure import ValueStructure
from src.mobj_types.mobj_type import MobjType
from src.mobjs.mobj import Mobj

VariableType = MobjType("Variable", ValueStructure.non_defining(0))


class Variable(Mobj):
    """Represents a mathematical variable"""

    def __init__(self, name: str):
        # Dont allow empty variable names
        if name == "":
            raise ValueError("Variable name cannot be empty")
        self.var_name = name

    @property
    def type(self) -> MobjType:
        return VariableType

    @property
    def variables(self) -> set[str]:
        return {self.var_name}

    @property
    def defined_variables(self) -> set[str]:
        return set()

    @property
    def values(self) -> tuple[Mobj]:
        return tuple()

    def evaluate(self, values: dict[str, Mobj]) -> Mobj:
        return values[self.var_name] if self.var_name in values else self

    def create_dictionary_from(self, evaluation: Mobj):
        return {self.var_name: evaluation}

    def __eq__(self, other: object) -> bool:
        return self.var_name == other.var_name if isinstance(other, Variable) else False
