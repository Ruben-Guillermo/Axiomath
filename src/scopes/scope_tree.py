from src.mobj_types.mobj_type import MobjType
from src.mobjs.mobj import Mobj
from src.mobjs.variable import Variable
from src.scopes.inference_rule import InferenceRule
from src.scopes.scope import Scope


class ScopeTree:
    """
    Class to hold universal data common to a hierarchy of scopes,
    such as a list of all known mobj types, inference rules and axioms.
    """

    def __init__(
        self,
        mobj_types: list[MobjType],
        inference_rules: dict[str, type[InferenceRule]],
    ):
        self._mobj_types = mobj_types
        self._inference_rules = inference_rules
        self._axioms = []

    def add_axiom(self, axiom: Mobj):
        # Check if the axiom uses valid types
        if not self.mobj_uses_valid_types(axiom):
            raise Exception(f"Axiom '{axiom}' uses invalid types")

        # Check the axiom is self defined
        if not axiom.variables == axiom.defined_variables:
            raise Exception(f"Axiom '{axiom}' is not self defined")

        """
        If the axiom is using a quantifier variable that is already used as something else in a child scope,
        it will be caught when the axiom is added to the child scope in the check_mobj_valid method.
        TODO: Test this a lot because it's a bit of a hack
        """

        self._axioms.append(axiom)

    def add_axioms(self, axioms: list[Mobj]):
        for axiom in axioms:
            self.add_axiom(axiom)

    @property
    def axiom_count(self) -> int:
        return len(self._axioms)

    @property
    def axioms(self) -> list[Mobj]:
        return self._axioms

    def is_rule(self, rule: InferenceRule) -> bool:
        for rule_name in self._inference_rules:
            if isinstance(rule, self._inference_rules[rule_name]):
                return True
        return False

    def create_base_scope(self) -> Scope:
        return Scope(self)

    def mobj_uses_valid_types(self, mobj: Mobj) -> bool:
        """Recursively checks if the mobj and all its values use valid types"""

        if mobj.type not in self._mobj_types and not isinstance(mobj, Variable):
            return False

        return all([self.mobj_uses_valid_types(value) for value in mobj.values])
