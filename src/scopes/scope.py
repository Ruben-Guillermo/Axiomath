from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from dataclasses import dataclass, field

from src.mobjs.mobj import Mobj

if TYPE_CHECKING:
    from src.scopes.inference_rule import InferenceRule
    from src.scopes.scope_tree import ScopeTree


@dataclass
class Scope:
    """
    This class is meant to hold a list of mobjs that are true statements
    given the assumptions of the scope and all its parents.
    It also allows for the creation of new true statements using inference rules.

    So, if ScopeA has 'A -> B' as an assumption, and ScopeB,
    whose parent is ScopeA has 'A' as an assumption, we can bring 'A -> B' into ScopeB,
    and then use it to infer 'B' with the 'Modus Ponens' rule.
    """

    _tree: ScopeTree
    _parent: Optional[Scope] = None
    _assumption: Optional[Mobj] = None
    _true_statements: list[Mobj] = field(default_factory=list)

    # Variables that are used in the scope THAT ARENT USED IN THE PARENT SCOPE

    # Variables with no restrictions (can be anything)
    _scope_free_variables: set[str] = field(default_factory=set)
    # Variables with restrictions (created from an exists)
    _scope_bounded_variables: set[str] = field(default_factory=set)
    # Variables that are used as quantifiers (like in 'exists x')
    _scope_quantifier_variables: set[str] = field(default_factory=set)

    @property
    def true_statements(self) -> list[Mobj]:
        return self._true_statements

    @property
    def number_of_true_statements(self) -> int:
        return len(self._true_statements)

    @property
    def tree(self) -> ScopeTree:
        return self._tree

    @property
    def assumption(self) -> Optional[Mobj]:
        return self._assumption

    @property
    def parent(self) -> Optional[Scope]:
        return self._parent

    def check_mobj_valid(self, mobj: Mobj):
        if not self._tree.mobj_uses_valid_types(mobj):
            raise Exception(f"Mobj '{mobj}' uses invalid types")

        # Check if all variables are used correctly
        # (We are not using a quantifier variable that already exists in the scope as something else)
        for var in mobj.variables:
            free_or_bounded = self.is_free_or_bounded_variable(var)
            quantifier = self.is_quantifier_variable(var)

            if var in mobj.defined_variables:
                if free_or_bounded or not quantifier:
                    raise Exception(
                        f"Variable '{var}' is used as a quantifier but is already used as something else"
                    )
            else:
                if not free_or_bounded or quantifier:
                    raise Exception(
                        f"Variable '{var}' is used as something else but is already used as a quantifier"
                    )

    def use_inference_rule(self, rule: InferenceRule, *indexes: int):
        mobjs = tuple(self._true_statements[i] for i in indexes)
        types = tuple(mobj.type for mobj in mobjs)

        if not self._tree.is_rule(rule):
            raise Exception(f"Rule '{rule}' does not exist")

        if not rule.types_are_valid(*types):
            raise Exception(f"Types of mobjs are not valid for rule '{rule}'")

        if not rule.is_applicable(self, *mobjs):
            raise Exception(f"Rule '{rule}' is not applicable to the given mobjs")

        rule.infer(self, *mobjs)

    def add_true_statement(self, mobj: Mobj):
        self.check_mobj_valid(mobj)

        self._true_statements.append(mobj)

    def is_free_variable(self, var: str) -> bool:
        """Recursively checks if the variable is free in this hierarchy"""
        return var in self._scope_free_variables or (
            self._parent is not None and self._parent.is_free_variable(var)
        )

    def is_bounded_variable(self, var: str) -> bool:
        """Recursively checks if the variable is bounded in this hierarchy"""
        return var in self._scope_bounded_variables or (
            self._parent is not None and self._parent.is_bounded_variable(var)
        )

    def is_free_or_bounded_variable(self, var: str) -> bool:
        """Recursively checks if the variable is free or bounded in this hierarchy"""
        return (
            var in self._scope_free_variables
            or var in self._scope_bounded_variables
            or (
                self._parent is not None
                and self._parent.is_free_or_bounded_variable(var)
            )
        )

    def is_quantifier_variable(self, var: str) -> bool:
        """Recursively checks if the variable is a quantifier in this hierarchy"""
        return var in self._scope_quantifier_variables or (
            self._parent is not None and self._parent.is_quantifier_variable(var)
        )

    def get_father_scope(self, generations: int) -> Optional[Scope]:
        if generations < 0:
            raise Exception("Generations must be a positive integer")
        if generations == 0:
            return self

        return (
            self._parent.get_father_scope(generations - 1)
            if self._parent is not None
            else None
        )
